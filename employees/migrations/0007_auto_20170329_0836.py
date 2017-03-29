# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-29 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20170322_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=16, verbose_name='gender'),
        ),
    ]
