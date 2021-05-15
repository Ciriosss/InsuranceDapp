from django import forms
from django.contrib.auth.models import User
from .models import Profile, Transaction
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', ]

class SetUpAccount(forms.ModelForm):
    privateKey = forms.CharField(max_length=64)

    class Meta :
        model = Profile
        fields = ['privateKey']

class BuyToken(forms.ModelForm):
    amount = forms.FloatField()

    class Meta :
        model = Transaction
        fields = ['amount']