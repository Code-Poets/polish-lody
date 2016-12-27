from django.contrib.auth import authenticate, login, views, models
from django.views.generic import RedirectView
from django.shortcuts import render
from django.conf import settings
from users.models import MyUser
import base64

#from django.template.response import TemplateResponse

def auto_login(request, kwargs):
    #username = views.login.form.username.cleared_data[[key for key in cleared_data]]
    #password = views.password.reset.password_reset_form.cleared_data[[key for key in cleared_data]]
    #user = authenticate(username=username, password=password)
    #uid = int(base64.b64decode(kwargs["uidb64"]+'=='))
    #user = MyUser.objects.filter(id = uid)[0] 
    if kwargs["user"] is not None:
       login(request, kwargs["user"], backend=settings.authentication_backends[0])
       RedirectView.as_view(url='/')
    else:
       render(request, "I just don't know what went wrong")
#@auto_login

'''def password_reset(request):

    result = views.password_reset.(request, template_name="registration/password_reset_form.html")
    username = result.form.email
    return result, username 
'''
#auto_login(password_reset_complete)
#@auto_login
def password_reset_confirm(request, **kwargs):
    assert "template_name" not in kwargs, "One does not bring their own template into this view"
    #template_response = views.password_reset_confirm(request, template_name="registration/password_reset_confirm.html", **kwargs)
    uid = int(base64.b64decode(kwargs["uidb64"]+'=='))
    username = MyUser.objects.filter(id = uid)[0]
    #password = template_response["request"].POST['password']
    #user = authenticate(username=username, password = password)
    #user = request.POST['username']
    if request.method == 'POST':
       login(request, username, backend=settings.AUTHENTICATION_BACKENDS[0])
       #RedirectView.as_view(url='/reset/done/')
    
    return views.password_reset_confirm(request, template_name="registration/password_reset_confirm.html", **kwargs) 
'''
def password_reset_complete(request):
    #auto_login(request)
    return views.password_reset_complete(request, template_name="registration/password_reset_complete.html")
'''
    #return render(template_response, "registration/password_reset_complete.html", {})
