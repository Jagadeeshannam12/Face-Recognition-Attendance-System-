from django import forms
from django.contrib.auth.models import User
from .models import Student

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    registration_number = forms.CharField(max_length=20)
    section = forms.CharField(max_length=10)
    face_image = forms.ImageField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_registration_number(self):
        reg_no = self.cleaned_data['registration_number']
        if Student.objects.filter(registration_number=reg_no).exists():
            raise forms.ValidationError("This registration number already exists.")
        return reg_no

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
