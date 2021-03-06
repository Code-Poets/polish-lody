# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-03-01 14:59
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='icecream',
            name='icecream_standard_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='icecream',
            name='icecream_standard_production_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='icecream',
            name='icecream_name',
            field=models.CharField(blank=True, default=None, max_length=64, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='icecreamcosts',
            name='icecream_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='icecreamcosts',
            name='icecream_production_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterUniqueTogether(
            name='icecream',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='icecream',
            name='icecream_shop',
        ),
    ]
