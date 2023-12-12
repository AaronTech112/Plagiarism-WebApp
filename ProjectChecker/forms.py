from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.forms import ModelForm

class RegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
           'fullname','username','email','department','matric_number','phone_number','password1','password2','profile_pic','gender'
            ]
        
class RegisterLecturerForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
           'fullname','username','email','staff_id_number','phone_number','password1','password2','profile_pic','gender'
            ]

        
        
class UpdateUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = [
           'username','fullname','email','phone_number','gender','profile_pic',
            ]