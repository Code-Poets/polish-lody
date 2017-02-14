from django.contrib import admin
from .models import Date, Shop, IceCream, IceCreamCosts
# Register your models here.

class DateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date', 'date_shop']}),
    ]

class ShopAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Shop name', {'fields': ['shop_name']}),
        ('Shop location', {'fields': ['shop_address']}),
    ]

class IceCreamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Ice cream details', {'fields': ['icecream_shop','icecream_name']})
    ]

class IceCreamCostsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Ice cream cost', {'fields': ['icecream_date','icecream_price','icecream_production_cost',
                                          'icecream_amount_sold']})
    ]

admin.site.register(Date, DateAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(IceCream, IceCreamAdmin)
admin.site.register(IceCreamCosts, IceCreamCostsAdmin)
