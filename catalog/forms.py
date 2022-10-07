from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type':'text', 'id': 'username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type':'email', 'id': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'id': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password', 'id': 'password2'}))



