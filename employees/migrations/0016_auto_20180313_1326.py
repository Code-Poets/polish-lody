# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-13 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0015_auto_20180313_1321'),
    ]

    operations = [
        migrations.AddField(
            model_name='month',
            name='month_not_approved_with_comment',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Approved?'),
        ),
        migrations.AlterField(
            model_name='month',
            name='month_is_approved',
            field=models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Approved?'),
        ),
    ]
