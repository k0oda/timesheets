# Generated by Django 3.0.8 on 2020-08-18 16:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0003_auto_20200809_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
