# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-03-16 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0019_auto_20180315_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='message_reason_hours_not_approved',
            field=models.TextField(blank=True, default=None, null=True, verbose_name='Comment, why you disagree with the hours (optional)'),
        ),
    ]
