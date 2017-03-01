# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-15 11:39
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='IceCream',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icecream_name', models.CharField(blank=True, default=None, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IceCreamCosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icecream_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('icecream_production_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('icecream_amount_sold', models.PositiveIntegerField(default=0)),
                ('icecream', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.IceCream')),
                ('icecream_date', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Date')),
            ],
            options={
                'verbose_name_plural': 'Ice cream costs',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('shop_address', models.TextField(blank=True, default=None, max_length=256, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='icecreamcosts',
            name='icecream_shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Shop'),
        ),
        migrations.AddField(
            model_name='icecream',
            name='icecream_shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.Shop'),
        ),
        migrations.AlterUniqueTogether(
            name='icecreamcosts',
            unique_together=set([('icecream_shop', 'icecream', 'icecream_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='icecream',
            unique_together=set([('icecream_shop', 'icecream_name')]),
        ),
    ]