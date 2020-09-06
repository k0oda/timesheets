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
from reportlab.lib.enums import TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Rect

from datetime import date

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
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=15, leftMargin=15, topMargin=50, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='MainTitle', textColor=colors.Color(0, 0, 0, 0.3), fontSize=50))
        styles.add(ParagraphStyle(name='HeaderRightText', textColor=colors.white))
        styles.add(ParagraphStyle(name='HeaderLeftText', textColor=colors.Color(0, 0, 0, 0.7), fontSize=8))
        styles.add(ParagraphStyle(name='HeaderRightTitle', textColor=colors.white, alignment=TA_RIGHT, fontSize=20))
        styles.add(ParagraphStyle(name='HeaderRightUnderTitle', textColor=colors.white, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='NotesText', textColor=colors.Color(0, 0, 0, 0.7), fontSize=10))
        styles.add(ParagraphStyle(name='FooterText', textColor=colors.white, alignment=TA_CENTER, backColor=colors.Color(0, 0.1, 0, 0.4), borderPadding=(5, 1, 5), fontSize=12))

        story = []

        text = request.user.company.name
        story.append(Paragraph(text, styles['MainTitle']))
        story.append(Spacer(1, 65))

        header_data = [
            [Paragraph(f'{invoice.date.strftime("%b %d, %Y")}<br/>Invoice No. {invoice.pk}', styles['HeaderLeftText']), Paragraph('Ian Smith<br/>PO Box 6386<br/>Boise, ID 83707', styles['HeaderRightText'])],
            ['', Paragraph(f'INVOICE {invoice.client}', styles['HeaderRightTitle'])],
            ['', Paragraph(f'{invoice.client.address}', styles['HeaderRightUnderTitle'])],
            ['', ''],
        ]

        header = Table(header_data, colWidths=[85, 485], rowHeights=[70, 5, 40, 35], style=[
            ('GRID', (0, 0), (-1, -1), 0.5, colors.transparent),

            # Left cell text
            ('VALIGN', (0, 0), (0, 0), "MIDDLE"),
            ('SPAN', (0, 0), (0, 1)),

            # Right cell top text
            ('VALIGN', (1, 0), (1, 0), "TOP"),
            
            # Backgrounds
            ('BACKGROUND', (0, 0), (0, -1), colors.Color(0, 0, 0, 0.10)),
            ('BACKGROUND', (1, 0), (1, -1), colors.Color(0, 0.1, 0, 0.4)),

            # Client info
            ('VALIGN', (1, 1), (1, 1), "TOP"),
            ('ALIGN', (1, 1), (1, 1), "RIGHT"),
        ])
        story.append(header)
        story.append(Spacer(1, 12))

        employees = {}
        first_date = date.min
        last_date = date.min
        total_bill = 0
        total_hours = 0
        for item in invoice.items.all():
            employees_objects = []
            for entry in item.project.entries.order_by('date'):
                if entry.user not in employees_objects:
                    employees[entry.user.username] = {
                        'name': f'{entry.user.first_name} {entry.user.last_name}',
                        'total_hours': entry.timer.hour,
                        'bill': entry.timer.hour * entry.user.hourly_rate,
                        'project': item.project.name,
                        'first_date': entry.date,
                        'last_date': entry.date,
                    }
                    total_hours += entry.timer.hour
                    total_bill += entry.timer.hour * entry.user.hourly_rate
                    if first_date < entry.date:
                        first_date = entry.date
                    if last_date < entry.date:
                        last_date = entry.date
                    employees_objects.append(entry.user)
                else:
                    employees[entry.user.username]['total_hours'] += entry.timer.hour
                    employees[entry.user.username]['bill'] += entry.timer.hour * entry.user.hourly_rate
                    employees[entry.user.username]['last_date'] = entry.date
                    if first_date < employees[entry.user.username]['first_date']:
                        first_date = employees[entry.user.username]['first_date']
                    if last_date < employees[entry.user.username]['last_date']:
                        last_date = employees[entry.user.username]['last_date']
                    total_hours += entry.timer.hour
                    total_bill += entry.timer.hour * entry.user.hourly_rate

        bills_data = [
            ['Date', 'Project', 'Hours', 'Bill'],
        ]

        for employee in employees.values():
            bill = []

            text = f'{employee["first_date"].month}/{employee["first_date"].day}-{employee["last_date"].month}/{employee["last_date"].day}'
            bill.append(Paragraph(text, styles['Normal']))

            text = str(employee['name']) + ' | ' + str(employee['project'])
            bill.append(Paragraph(text, styles['Normal']))

            text = str(employee['total_hours'])
            bill.append(Paragraph(text, styles['Normal']))

            text = str(employee["bill"])
            bill.append(Paragraph(text, styles['Normal']))

            bills_data.append(bill)
        
        bills_data.append([])
        bills_data.append(['', 'Total', total_hours, total_bill])

        bills = Table(bills_data, colWidths=[55, 435, 40], style=[
            ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ])
        story.append(bills)
        story.append(Spacer(1, 12))

        pay_info_data = [
            [f'Payable: {invoice.company.name}', f'${total_bill} due for {first_date.month}-{first_date.day}-{first_date.year} to {last_date.month}-{last_date.day}-{last_date.year}'],
            ['Address', 'Vidicode, Inc PO Box 6386, Boise, ID 83707 ']
        ]

        pay_info = Table(pay_info_data, colWidths=[100, 470], style=[
            ('GRID', (0, 0), (-1, -1), 0.3, colors.black),
        ])
        story.append(pay_info)
        story.append(Spacer(1, 12))

        story.append(Paragraph(invoice.notes, styles['NotesText']))
        story.append(Spacer(1, 310))

        story.append(Paragraph('Vidicode Inc&nbsp;&nbsp;&nbsp;&nbsp;360-551-7339', styles['FooterText']))

        doc.build(story)
        buffer.seek(0)

        for item in invoice.items.all():
            for entry in item.project.entries.all():
                entry.delete()
            item.delete()
        invoice.delete()

        return FileResponse(buffer, as_attachment=True, filename=f'Invoice {invoice.pk} {invoice.client}.pdf')
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
