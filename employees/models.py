from __future__ import unicode_literals

from django.db import models
from django.core.validators import validate_email

class Employee(models.Model):
    first_name = models.CharField(max_length=250, default=None)
    last_name = models.CharField(max_length=250, default=None)
    email = models.EmailField(validators=[validate_email], max_length=75, unique=True, default=None)
    rate_per_hour = models.DecimalField(max_digits=7, decimal_places=2, blank=True, default=0)
    contract_exp_date = models.DateField(blank=True, default=None, null=True)
    health_book_exp_date = models.DateField(blank=True, default=None, null=True)

    def __str__(self):
        return self.first_name

    def full_name(self):
        return self.first_name + " " + self.last_name