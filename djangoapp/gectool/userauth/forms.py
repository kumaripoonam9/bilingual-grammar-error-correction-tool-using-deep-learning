# class UserRegistrationForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
 

class SignUpForm(UserCreationForm):
    USER_TYPES_CHOICES = (
        ('normal_user', 'Normal User'),
        ('expert_user', 'Expert User')
    )
    user_type = forms.ChoiceField(choices=USER_TYPES_CHOICES, label="Type of user")
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'user_type',  'password1', 'password2' )