# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-29 16:22
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('myuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('rate_per_hour', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('contract_start_date', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('contract_exp_date', models.DateField(blank=True, default=None, null=True)),
                ('health_book_exp_date', models.DateField(blank=True, default=None, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], default=None, max_length=16, null=True)),
                ('position', models.CharField(blank=True, choices=[('Production', 'Production'), ('Sale', 'Sale'), ('Other', 'Other')], default=None, max_length=16, null=True)),
                ('contract_type', models.CharField(blank=True, choices=[('Fixed-term employment contract', 'Fixed-term employment contract'), ('Non-fixed-term employment contract', 'Non-fixed-term employment contract'), ('Other', 'Other')], default=None, max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('users.myuser',),
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(default=2016, validators=[django.core.validators.MaxValueValidator(9999)])),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12, verbose_name='Month')),
                ('salary_is_paid', models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False, verbose_name='Paid?')),
                ('hours_worked_in_this_month', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(720)])),
                ('rate_per_hour_this_month', models.DecimalField(decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(0)])),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='month',
            unique_together=set([('employee', 'month', 'year')]),
        ),
    ]
