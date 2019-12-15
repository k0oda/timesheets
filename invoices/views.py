from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice, Item
from manage_app.models import Client
from django.utils.dateparse import parse_date

@login_required
def invoices(request):
    invoices = Invoice.objects.filter(company=request.user.company)
    items = Item.objects.filter(company=request.user.company)
    clients = Client.objects.filter(company=request.user.company)

    return render(request, 'invoices/invoices.html', context={
        'invoices': invoices,
        'items': items,
        'clients': clients
    })

@login_required
def add_invoice(request):
    if request.user.role.invoices_manage_access:
        if request.method.lower() == 'post':
            client = get_object_or_404(Client, name=request.POST.get('client'), company=request.user.company)
            date = parse_date(request.POST.get('date'))
            notes = request.POST.get('notes')
            new_invoice = Invoice.objects.create(
                company=request.user.company,
                client=client,
                date=date,
                notes=notes
            )
            new_invoice.save()
            return redirect('add_item', new_invoice.pk)
        else:
            clients = Client.objects.filter(company=request.user.company)

            return render(request, 'invoices/new_invoice.html', context={
                'clients': clients
            })
    else:
        return redirect('invoices')

@login_required
def edit_invoice(request, pk):
    if request.user.role.invoices_manage_access:
        if request.method.lower() == 'post':
            invoice = get_object_or_404(Invoice, company=request.user.company, pk=pk)
            invoice.client = get_object_or_404(Client, name=request.POST.get('client'), company=request.user.company)
            invoice.date = parse_date(request.POST.get('date'))
            invoice.notes = request.POST.get('notes')
            invoice.save()
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
            new_item = Item.objects.create(
                company=invoice.company,
                invoice=invoice,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                amount=request.POST.get('amount'),
                unit_price=request.POST.get('unit_price'),
                total_price=int(request.POST.get('amount')) * float(request.POST.get('unit_price'))
            )
            new_item.save()

            invoice.total_amount += int(new_item.amount)
            invoice.total_unit_price += float(new_item.unit_price)
            invoice.total_price += int(new_item.amount) * float(new_item.unit_price)
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
            item.invoice.total_amount -= int(item.amount)
            item.invoice.total_unit_price -= float(item.unit_price)
            item.invoice.total_price -= int(item.amount) * float(item.unit_price)

            item.name = request.POST.get('name')
            item.description = request.POST.get('description')
            item.amount = request.POST.get('amount')
            item.unit_price = request.POST.get('unit_price')
            item.total_price = int(item.amount) * float(item.unit_price)
            item.save()

            item.invoice.total_amount += int(item.amount)
            item.invoice.total_unit_price += float(item.unit_price)
            item.invoice.total_price += item.total_price
            item.invoice.save()
        return redirect('add_item', item.invoice.pk)
    else:
        return redirect('invoices')

@login_required
def delete_item(request, pk):
    if request.user.role.invoices_manage_access:
        item = get_object_or_404(Item, company=request.user.company, pk=pk)
        item.delete()
        return redirect('add_item', item.invoice.pk)
    else:
        return redirect('invoices')
