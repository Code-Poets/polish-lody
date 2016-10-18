from django.conf.urls import url

from . import views

urlpatterns = [
    # employee list
    url(r'^$', views.EmployeeList.as_view(), name='employees'),
    url(r'^(?P<pk>\d+)$', views.EmployeeDetail.as_view(), name='employee_detail'),
    url(r'^new$', views.EmployeeCreate.as_view(), name='employee_new'),
    url(r'^edit/(?P<pk>\d+)$', views.EmployeeUpdate.as_view(), name='employee_edit'),
    url(r'^delete/(?P<pk>\d+)$', views.EmployeeDelete.as_view(), name='employee_delete'),
]