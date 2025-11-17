from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import CustomUser


class UserForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    phone = forms.CharField(required=False, label="Phone")
    address = forms.CharField(required=False, label="Address")

    class Meta:
        # model = User
        model = CustomUser
        # fields = ("username", "password1", "password2", "email")
        fields = ("username", "password1", "password2", "email", "phone", "address")
        
