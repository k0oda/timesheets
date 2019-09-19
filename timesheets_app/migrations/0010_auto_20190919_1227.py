# Generated by Django 2.2.4 on 2019-09-19 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets_app', '0009_auto_20190918_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='name',
        ),
        migrations.AlterField(
            model_name='company',
            name='date_of_creation',
            field=models.DateField(default=datetime.date(2019, 9, 19)),
        ),
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.date(2019, 9, 19)),
        ),
    ]
