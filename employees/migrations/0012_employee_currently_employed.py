# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-02-23 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0011_auto_20180222_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='currently_employed',
            field=models.BooleanField(default=True),
        ),
    ]