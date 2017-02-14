from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',                                views.SalesIndex.as_view(),   name='sales'),
]

