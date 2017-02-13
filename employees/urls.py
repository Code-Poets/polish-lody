from django.conf.urls import url

from . import views

pk = r'(?P<pk>\d+)'

urlpatterns = [
    # employee list
    url(r'^$',                                views.EmployeeList.as_view(),   name='employees'),
    url(r'^new$',                             views.EmployeeCreate.as_view(), name='employee_new'),
    url(r'^new/emailverify/$',                views.ajax_verify_email,        name='emailverify'),
    url(r'^' + pk + r'$',                     views.EmployeeDetail.as_view(), name='employee_detail'),
    url(r'^' + pk + r'/new_month$',           views.MonthCreate.as_view(),    name='month_new'),
    url(r'^edit/'       + pk + r'$',          views.EmployeeUpdate.as_view(), name='employee_edit'),
    url(r'^months/'     + pk + r'$',          views.MonthUpdate.as_view(),    name='month_edit'),    
    url(r'^delete/'     + pk + r'$',          views.EmployeeDelete.as_view(), name='employee_delete'),
    url(r'^del_month/'  + pk + r'$',          views.MonthDelete.as_view(),    name='month_delete'),
    url(r'^appr_month/' + pk + r'/$',         views.MonthApprove.as_view(),   name='month_approve'),
]

handler404 = 'employees.views.pl_404_view'
handler500 = 'employees.views.pl_500_view'
