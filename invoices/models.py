from django.db import models
from manage_app.models import Client
from company_panel.models import Company


class Invoice(models.Model):
    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
        ordering = ['company', 'date']

    client = models.ForeignKey(Client, models.CASCADE, related_name='+')
    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    date = models.DateField()
    total_amount = models.IntegerField(null=True, default=0)
    total_unit_price = models.DecimalField(null=True, default=0, max_digits=20, decimal_places=2)
    total_price = models.DecimalField(null=True, default=0, max_digits=20, decimal_places=2)
    notes = models.TextField(max_length=350, blank=True)

    def __str__(self):
        return self.client.name

    def get_items(self):
        return Item.objects.filter(invoice=self)


class Item(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['company', 'invoice']

    company = models.ForeignKey(Company, models.CASCADE, related_name='+')
    invoice = models.ForeignKey(Invoice, models.CASCADE, related_name='items')
    project = models.ForeignKey(Project, models.CASCADE, related_name='+')
    total_price = models.DecimalField(null=True, default=0, max_digits=20, decimal_places=2)

    def __str__(self):
        return self.project.name
