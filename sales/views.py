from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from employees.mixins import StaffRequiredMixin
# Create your views here.
from .models import Shop, IceCream, IceCreamCosts, Date
from django.views.generic import ListView
from datetime import datetime, date, timedelta
import time

def list_last_two_weeks():#shop_name, icecream_name):
    # now = datetime.today()
    curr_time = time.time()
    now = datetime(2017,2,15) # mockup date so the function works for now, should be changed later
    ###
    ### These functions create a list of 14 days past the current date. For now the date is hardcoded
    ### so that the graphs on page work. This function could be time consuming, so I suspect some 
    ### kind of caching might be necessary.
    ###
    day_list = [(now - timedelta(days=x)).strftime("%d-%m") for x in range(0, 14)]
    day_list_for_filtering = [(now - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 14)]
    # day_list_for_filtering = day_list_for_filtering[::-1]
    shop_name = Shop.objects.get(shop_name__contains="Mandryl")
    icecream_name = IceCream.objects.get(icecream_name__contains="Super")
    graph_data = []
    ###
    ### The for loop creates a list of lists in format ['mm-dd', 'int']. One of the graphs uses
    ### a third element in a list called annotation but it is added in the template.
    for day, day_short in zip(day_list_for_filtering[::-1], day_list[::-1]):
    # for day in day_list:
        try:
            db_date = Date.objects.get(date__contains=day)
            db_icecream = IceCreamCosts.objects.get(icecream=icecream_name,
                                                    icecream_shop=shop_name,
                                                    icecream_date=db_date)
            amount_sold = db_icecream.icecream_amount_sold
            graph_data.append([day_short, amount_sold, 'label'])
        except Date.DoesNotExist or IceCreamCosts.DoesNotExist:
            return False
    end_time = time.time()
    print(end_time-curr_time)
    return graph_data

class SalesIndex(LoginRequiredMixin, StaffRequiredMixin, ListView):

    model = Shop
    template_name = 'sales/sales_index.html'
    context_object_name = 'shops'

    def get_context_data(self, **kwargs):
        context = super(SalesIndex, self).get_context_data(**kwargs)
        context['dates'] = Date.objects.all()
        context['bestsellers_1'] = IceCream.objects.all()
        context['bestsellers_2'] = IceCream.objects.all()
        context['graph_data'] = list_last_two_weeks()

        return context
