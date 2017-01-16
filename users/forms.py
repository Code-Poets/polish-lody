from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm
from django import forms
 
from users.models import MyUser
 
class UserCreationForm(AuthUserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super(UserCreationForm, self).clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

    class Meta:
        model = MyUser
        fields = ["email"]

class UserChangeForm(AuthUserChangeForm):

    class Meta:
        model = MyUser
        fields = ["email"]
