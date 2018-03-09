# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-27 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0009_auto_20170426_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='contract_type',
            field=models.CharField(blank=True, choices=[('Fixed-term employment contract', 'Fixed-term employment contract'), ('Non-fixed-term employment contract', 'Non-fixed-term employment contract'), ('Contract work', 'Contract work'), ('Fee-for-task contract', 'Fee-for-task contract '), ('B2B', 'B2B'), ('Other', 'Other')], default=None, max_length=64, null=True, verbose_name='contract type'),
        ),
    ]