# Generated by Django 3.0.8 on 2020-08-18 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_auto_20200818_1652'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='total_unit_price',
        ),
    ]
