from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from company_panel.models import Company
from invoices.models import Invoice, Item


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

        return render(request, 'invoices/invoices.html', context={
            'company': company,
            'invoices': invoices,
            'items': items
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
            date = request.POST.get('date')
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