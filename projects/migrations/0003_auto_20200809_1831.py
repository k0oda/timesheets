# Generated by Django 3.0.8 on 2020-08-09 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20191207_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['company', 'name'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
    ]
