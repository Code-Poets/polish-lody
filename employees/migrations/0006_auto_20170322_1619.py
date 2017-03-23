# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-22 16:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_auto_20170321_1045'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'city', 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'employee', 'verbose_name_plural': 'employees'},
        ),
        migrations.AlterModelOptions(
            name='month',
            options={'verbose_name': 'month', 'verbose_name_plural': 'months'},
        ),
        migrations.AlterField(
            model_name='employee',
            name='address_city',
            field=models.ForeignKey(blank=True, default=None, max_length=30, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.City', to_field='name', verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='address_street',
            field=models.CharField(blank=True, default=None, max_length=80, null=True, verbose_name='Street'),
        ),
    ]
