# Generated by Django 3.0.8 on 2020-08-09 15:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company_panel', '0010_auto_20191207_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'ordering': ['date_of_creation'], 'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'ordering': ['company', 'name'], 'verbose_name': 'Role', 'verbose_name_plural': 'Roles'},
        ),
        migrations.AlterField(
            model_name='company',
            name='date_of_creation',
            field=models.DateField(default=datetime.date(2020, 8, 9)),
        ),
    ]
