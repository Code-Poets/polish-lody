# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-22 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_auto_20161222_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='salary_is_paid',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Paid?'),
        ),
    ]