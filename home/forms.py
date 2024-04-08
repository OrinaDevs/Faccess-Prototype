from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UploadImageForm(forms.Form):
    image = forms.ImageField()

