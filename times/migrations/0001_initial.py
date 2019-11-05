# Generated by Django 2.2.4 on 2019-11-05 11:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
        ('manage_app', '0001_initial'),
        ('company_panel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2019, 11, 5))),
                ('notes', models.CharField(blank=True, default=' ', max_length=350)),
                ('timer', models.TimeField(default=datetime.time(0, 0))),
                ('start_time', models.TimeField(default=datetime.time(0, 0))),
                ('is_active', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company_panel.Company')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='projects.Project')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='manage_app.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
