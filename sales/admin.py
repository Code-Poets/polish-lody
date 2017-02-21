from django.contrib import admin
from .models import Date, Shop, IceCream, IceCreamCosts
# Register your models here.

class DateAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['date']}),
    ]

class ShopAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Shop name', {'fields': ['shop_name']}),
        ('Shop location', {'fields': ['shop_address']}),
    ]

class IceCreamAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Ice cream details', {'fields': ['icecream_name',
                                          'icecream_standard_price']})
    ]

class IceCreamCostsAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Ice cream cost', {'fields': ['icecream',
                                       'icecream_shop',
                                       'icecream_date',
                                       'icecream_price',
                                       'icecream_production_cost',
                                       'icecream_amount_sold']})
    ]

admin.site.register(Date, DateAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(IceCream, IceCreamAdmin)
admin.site.register(IceCreamCosts, IceCreamCostsAdmin)
