from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.

class Shop(models.Model):
    ### Name: (e.g. "Shop at Bema street" or "Superhero hideout")
    shop_name = models.CharField(blank=True, null=True, default=None, max_length=64)
    shop_address = models.TextField(blank=True, null=True, default=None, max_length=256)

    def __str__(self):
        return self.shop_name

class Date(models.Model):

    date_shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(blank=True, default=timezone.now, null=True)

    def __str__(self):
        return str(self.date_shop) + ' ' + str(self.date)

    class Meta:
        unique_together = (("date", "date_shop"),)

class IceCream(models.Model):

    icecream_shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)
    icecream_name = models.CharField(blank=True, null=True, default=None, max_length=64)

    def __str__(self):
        return self.icecream_name

    class Meta:
        unique_together = (("icecream_shop", "icecream_name"),)

class IceCreamCosts(models.Model):

    icecream = models.ForeignKey(IceCream, on_delete=models.CASCADE)
    icecream_shop = models.ForeignKey(Shop, null=True, blank=True, on_delete=models.CASCADE)
    icecream_date = models.ForeignKey(Date, null=True, blank=True, on_delete=models.CASCADE)
    icecream_price = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                         validators=[MinValueValidator(0)])
    icecream_production_cost = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                                   validators=[MinValueValidator(0)])
    icecream_amount_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Sold " + str(self.icecream_amount_sold) + " of this ice cream."

    class Meta:
        unique_together = (("icecream_shop", "icecream", "icecream_date"),)
        verbose_name_plural = "Ice cream costs"

