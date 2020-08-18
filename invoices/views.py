from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf import settings
from django.http import FileResponse
from invoices.models import Invoice, Item
from manage_app.models import Client
from invoices.forms import CreateInvoice, CreateItem

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

@login_required
def invoices(request):
    page = request.GET.get('page')
    if not page:
        page = 1
    page = int(page)

    items = Item.objects.filter(company=request.user.company)
    clients = Client.objects.filter(company=request.user.company)
    pages = Paginator(Invoice.objects.filter(company=request.user.company), settings.ITEMS_PER_PAGE)
    invoices = pages.page(page).object_list

    return render(request, 'invoices/invoices.html', context={
        'invoices': invoices,
        'items': items,
        'clients': clients,
        'pages': pages,
        'current_page': page,
    })

@login_required
def add_invoice(request):
    if request.user.role.invoices_manage_access:
        if request.method.lower() == 'post':
            form = CreateInvoice(request.user, data=request.POST)
            invoice = form.save(commit=False)
            invoice.company = request.user.company
            invoice.save()
            return redirect('add_item', invoice.pk)
        else:
            return render(request, 'invoices/new_invoice.html')
    else:
        return redirect('invoices')

@login_required
def edit_invoice(request, pk):
    if request.user.role.invoices_manage_access:
        if request.method.lower() == 'post':
            invoice = get_object_or_404(Invoice, company=request.user.company, pk=pk)
            form = CreateInvoice(request.user, invoice, data=request.POST)
            new_invoice = form.save(commit=False)
            invoice.client = new_invoice.client
            invoice.date = new_invoice.date
            invoice.notes = new_invoice.notes
            invoice.save()
    return redirect('invoices')

@login_required
def approve_invoice(request, pk):
    if request.user.role.invoices_manage_access:
        invoice = get_object_or_404(Invoice, company=request.user.company, pk=pk)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        story = []

        text = request.user.company.name
        story.append(Paragraph(text, styles['Heading2']))

        text = str(invoice.date)
        story.append(Paragraph(text, styles['Normal']))

        text = f'To {invoice.client}'
        story.append(Paragraph(text, styles['Normal']))

        text = invoice.client.address
        story.append(Paragraph(text, styles['Normal']))
        story.append(Spacer(1, 12))

        text = 'Bills:'
        story.append(Paragraph(text, styles['Heading3']))

        employees = {}
        total_bill = 0
        for item in invoice.items.all():
            employees_objects = []
            for entry in item.project.entries.all():
                if entry.user not in employees_objects:
                    employees[entry.user.username] = {
                        'name': f'{entry.user.first_name} {entry.user.last_name}',
                        'total_hours': entry.timer.hour,
                        'bill': entry.timer.hour * entry.user.hourly_rate,
                    }
                    total_bill += entry.timer.hour * entry.user.hourly_rate
                    employees_objects.append(entry.user)
                else:
                    employees[entry.user.username]['total_hours'] += entry.timer.hour
                    employees[entry.user.username]['bill'] += entry.timer.hour * entry.user.hourly_rate
                    total_bill += entry.timer.hour * entry.user.hourly_rate

        for employee in employees.values():
            text = employee['name']
            story.append(Paragraph(text, styles['Heading5']))

            text = f'Total hours: {employee["total_hours"]}'
            story.append(Paragraph(text, styles['Normal']))

            text = f'Bill: {employee["bill"]}'
            story.append(Paragraph(text, styles['Normal']))
            story.append(Spacer(1, 12))

        text = f'Total bill: {total_bill}'
        story.append(Paragraph(text, styles['Heading3']))
        story.append(Spacer(1, 12))

        doc.build(story)
        buffer.seek(0)

        for item in invoice.items.all():
            for entry in item.project.entries.all():
                entry.delete()
            item.delete()
        invoice.delete()

        return FileResponse(buffer, as_attachment=True, filename=f'{invoice.client}_{invoice.date}.pdf')
    return redirect('invoices')

@login_required
def delete_invoice(request, pk):
    if request.user.role.invoices_manage_access:
        invoice = get_object_or_404(Invoice, company=request.user.company, pk=pk)
        invoice.delete()
    return redirect('invoices')

@login_required
def add_item(request, invoice_pk):
    if request.user.role.invoices_manage_access:
        invoice = get_object_or_404(Invoice, company=request.user.company, pk=invoice_pk)
        items = Item.objects.filter(company=request.user.company, invoice=invoice)

        if request.method.lower() == 'post':
            form = CreateItem(request.user, data=request.POST)
            new_item = form.save(commit=False)
            new_item.company = invoice.company
            new_item.invoice = invoice
            entries = new_item.project.entries.all()
            for entry in entries:
                new_item.total_price += entry.timer.hour * entry.user.hourly_rate
            new_item.save()

            invoice.total_price += new_item.total_price
            invoice.save()
        return render(request, 'invoices/add_items.html', context={
            'invoice': invoice,
            'items': items
        })
    else:
        return redirect('invoices')

@login_required
def edit_item(request, pk):
    if request.user.role.invoices_manage_access:
        item = get_object_or_404(Item, company=request.user.company, pk=pk)

        if request.method.lower() == 'post':
            item.invoice.total_price -= item.total_price
            item.total_price = 0

            form = CreateItem(item, data=request.POST)
            new_item = form.save(commit=False)
            entries = new_item.project.entries.all()
            for entry in entries:
                item.total_price += entry.timer.hour * entry.user.hourly_rate
            item.save()

            item.invoice.total_price += item.total_price
            item.invoice.save()
        return redirect('add_item', item.invoice.pk)
    else:
        return redirect('invoices')

@login_required
def delete_item(request, pk):
    if request.user.role.invoices_manage_access:
        item = get_object_or_404(Item, company=request.user.company, pk=pk)
        item.invoice.total_price -= item.total_price
        item.invoice.save()
        item.delete()
        return redirect('add_item', item.invoice.pk)
    else:
        return redirect('invoices')
