from django.conf.urls import url

from . import views

urlpatterns = [
    # employee list
    url(r'^$', views.EmployeeList.as_view(), name='employees'),
    url(r'^(?P<pk>\d+)$', views.EmployeeDetail.as_view(), name='employee_detail'),
    url(r'^new$', views.EmployeeCreate.as_view(), name='employee_new'),
    url(r'^edit/(?P<pk>\d+)$', views.EmployeeUpdate.as_view(), name='employee_edit'),
    url(r'^months/(?P<pk>\d+)$', views.MonthUpdate.as_view(template_name='employees/month_edit_form.html'), name='month_edit'),
    url(r'^(?P<pk>\d+)/new_month$', views.MonthCreate.as_view(template_name='employees/month_form.html'), name='month_new'),
    url(r'^delete/(?P<pk>\d+)$', views.EmployeeDelete.as_view(), name='employee_delete'),
    url(r'^del_month/(?P<pk>\d+)$', views.MonthDelete.as_view(), name='month_delete'),
    url(r'^employees/per_page=(?P<per_page>[0-9]+)page=(?P<page>[0-9]+)/$', views.EmployeeList.as_view()),
    url(r'^(?P<pk>\d+)/per_page=(?P<per_page>[0-9]+)page=(?P<page>[0-9]+)/$', views.EmployeeList.as_view()),
    url(r'^new/emailverify/$', views.ajax_verify_email, name='emailverify'),
    url(r'^appr_month/(?P<pk>\d+)/$', views.MonthApprove.as_view(), name='month_approve'),
]

handler404 = 'employees.views.pl_404_view'
handler500 = 'employees.views.pl_500_view'
