# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 10:30
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_auto_20161019_1039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=255, verbose_name='Month')),
                ('salary_is_paid', models.BooleanField(default=False, verbose_name='Paid?')),
                ('hours_worked_in_this_month', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(720)])),
                ('how_much_was_paid_to_employee', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('rate_per_hour_this_month', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(blank=True, max_length=4, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='contract_start_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='contract_type',
            field=models.CharField(blank=True, choices=[('1', 'Type 1'), ('2', 'Type 2'), ('3', 'Type 3')], default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='employee_password',
            field=models.CharField(blank=True, default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, choices=[('1', 'Male'), ('2', 'Female')], default=None, max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='hours_in_current_month',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(720)]),
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.CharField(blank=True, choices=[('1', 'Production'), ('2', 'Sale'), ('3', 'Other')], default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='rate_per_hour',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='year',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='month',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Employee'),
        ),
        migrations.AddField(
            model_name='month',
            name='year',
            field=models.ForeignKey(default=2016, on_delete=django.db.models.deletion.CASCADE, to='employees.Year'),
        ),
    ]
