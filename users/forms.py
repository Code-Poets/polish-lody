from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django import forms
 
from users.models import MyUser
 
class UserCreationForm(AuthUserCreationForm):

    class Meta:
        model = MyUser
        fields = ["email"]

class UserChangeForm(AuthUserChangeForm):

    class Meta:
        model = MyUser
        fields = ["email"]
