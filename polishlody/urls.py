"""polishlody URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from . import views

urlpatterns = [
    url(r'^$', auth_views.login,{'redirect_authenticated_user': True}, name='login'),
    url(r'^accounts/login/$', RedirectView.as_view(url='/')),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^change-password/$', auth_views.password_change, {'template_name': 'registration/change-password.html'}, name='password_change'),
    url(r'^change-password/done/$', auth_views.password_change_done, {'template_name': 'registration/change-password-done.html'}, name='password_change_done'),
    url(r'^resetpassword/passwordsent/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^resetpassword/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^employees/', include('employees.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^sales/', include('sales.urls')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

# urlpatterns += i18n_patterns(
# )

handler404 = 'employees.views.pl_404_view'
handler500 = 'employees.views.pl_500_view'