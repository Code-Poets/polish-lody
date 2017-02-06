from django.contrib.auth import authenticate, login, views, models
from django.views.generic import RedirectView
from django.shortcuts import render
from django.conf import settings
from users.models import MyUser
import base64

def password_reset_confirm(request, **kwargs):
    assert "template_name" not in kwargs, "One does not bring their own template into this view"
    uid = int(base64.b64decode(kwargs["uidb64"] + '=='))
    userobject = MyUser.objects.filter(id = uid)[0]
    response = views.password_reset_confirm(request, template_name="registration/password_reset_confirm.html", **kwargs) 
    if request.method == 'POST' and response.status_code == 302:
       username = userobject.get_username()
       password = request.POST['new_password1']
       user = authenticate(username = username, password = password)
       login(request, user)
    return response
