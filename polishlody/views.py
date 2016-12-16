from django.contrib.auth import authenticate, login, views
from django.views.generic import RedirectView
from django.shortcuts import render
from users.models import MyUser

#from django.template.response import TemplateResponse

def auto_login(response):
    #username = views.login.form.username.cleared_data[[key for key in cleared_data]]
    #password = views.password.reset.password_reset_form.cleared_data[[key for key in cleared_data]]
    #user = authenticate(username=username, password=password)
    user = 
    if user is not None:
       login(response, user)
       RedirectView.as_view(url='/')
    else:
       render(response, "I just don't know what went wrong")
#@auto_login
'''def password_reset(request):

    result = views.password_reset.(request, template_name="registration/password_reset_form.html")
    username = result.form.email
    return result, username 
'''
#@auto_login
def password_reset_confirm(request, **kwargs):
    assert "template_name" not in kwargs, "One does not bring their own template into this view"
    login(request, user=user.email)
    #RedirectView.as_view(url='/')
    return views.password_reset_confirm(request, template_name="registration/password_reset_confirm.html")
def password_reset_complete(request):
    #auto_login(request)
    return views.password_reset_complete(request, template_name="registration/password_reset_complete.html")
    #return render(template_response, "registration/password_reset_complete.html", {})
