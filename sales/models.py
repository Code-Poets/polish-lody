from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import time
# Create your models here.

class Shop(models.Model):
    ### Name: (e.g. "Shop at Bema street" or "Superhero hideout")
    shop_name = models.CharField(blank=True, null=True, default=None, max_length=64)
    shop_address = models.TextField(blank=True, null=True, default=None, max_length=256)

    def __str__(self):
        return self.shop_name

class Date(models.Model):

    date = models.DateField(blank=True, default=timezone.now, null=True, unique=True)

    def __str__(self):
        return str(self.date)

    def date_short(self):
        return str(self.date.day) + '.' + str(self.date.month) + '.' + str(self.date.year)

    def is_date_recent(self):
        current_time = timezone.now()
        expiration_date = self.date
        # current_time = time.time()
        expiration_date = int(time.mktime(time.strptime(str(expiration_date), '%Y-%m-%d')))
        days_left = (expiration_date - current_time) / 259200
        if days_left < 3:
            return True
        else:
            return False

class IceCream(models.Model):

    icecream_name = models.CharField(blank=True, null=True, default=None, max_length=64, unique=True)
    icecream_standard_price = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                         validators=[MinValueValidator(0)])
    icecream_standard_production_cost = models.DecimalField(decimal_places=2, max_digits=8, default=0,
                                                   validators=[MinValueValidator(0)])

    def __str__(self):
        return self.icecream_name

class IceCreamCosts(models.Model):

    icecream = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    icecream_shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)
    icecream_date = models.ForeignKey(Date, null=True, blank=True, on_delete=models.CASCADE)
    icecream_price = models.DecimalField(decimal_places=2, max_digits=8, default=0,
                                         validators=[MinValueValidator(0)])
    icecream_production_cost = models.DecimalField(decimal_places=2, max_digits=8, default=0,
                                                   validators=[MinValueValidator(0)])
    icecream_amount_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.icecream) + ' at ' + str(self.icecream_shop) + ': ' + str(self.icecream_date)

    def icecream_revenue(self):
        return self.icecream_amount_sold*self.icecream_price

    class Meta:
        unique_together = (("icecream_shop", "icecream", "icecream_date"),)
        verbose_name_plural = "Ice cream costs"

