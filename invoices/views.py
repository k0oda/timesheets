from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from invoices.models import Invoice, Item
from manage_app.models import Client
from django.utils.dateparse import parse_date


class Invoices:
    @staticmethod
    @login_required
    def invoices(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        
        invoices = Invoice.objects.filter(company=company)
        items = Item.objects.filter(company=company)
        clients = Client.objects.filter(company=company)

        return render(request, 'invoices/invoices.html', context={
            'company': company,
            'invoices': invoices,
            'items': items,
            'clients': clients
        })

    @staticmethod
    @login_required
    def add_invoice(request):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

        if request.method.lower() == 'post':
            client = Client.objects.get(name=request.POST.get('client'), company=company)
            date = parse_date(request.POST.get('date'))
            notes = request.POST.get('notes')
            new_invoice = Invoice.objects.create(
                company=company,
                client=client,
                date=date,
                notes=notes
            )
            new_invoice.save()
            return redirect('add_item', new_invoice.pk)
        else:
            clients = Client.objects.filter(company=company)

            return render(request, 'invoices/new_invoice.html', context={
                'company': company,
                'clients': clients
            })

    @staticmethod
    @login_required
    def add_item(request, invoice_pk):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0
        
        invoice = Invoice.objects.get(company=company, pk=invoice_pk)
        items = Item.objects.filter(company=company, invoice=invoice)

        if request.method.lower() == 'post':
            new_item = Item.objects.create(
                company=company,
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
            'company': company,
            'invoice': invoice,
            'items': items
        })

    @staticmethod
    @login_required
    def edit_item(request, pk):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

        item = Item.objects.get(company=company, pk=pk)

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

    @staticmethod
    @login_required
    def delete_item(request, pk):
        company_id = request.user.company_id
        if Company.objects.filter(pk=company_id).exists():
            company = Company.objects.get(pk=company_id)
        else:
            company = 0

        item = Item.objects.get(company=company, pk=pk)
        item.delete()
        return redirect('add_item', item.invoice.pk)
