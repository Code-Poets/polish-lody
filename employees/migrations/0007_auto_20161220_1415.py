# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-20 14:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0006_auto_20161219_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='month',
            name='hours_worked_in_this_month',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(720)]),
        ),
        migrations.AlterField(
            model_name='month',
            name='rate_per_hour_this_month',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='month',
            name='year',
            field=models.IntegerField(default=2016, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
        ),
        migrations.AlterUniqueTogether(
            name='month',
            unique_together=set([('employee', 'month', 'year')]),
        ),
    ]
