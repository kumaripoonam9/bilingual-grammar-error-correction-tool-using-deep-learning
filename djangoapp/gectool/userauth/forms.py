# class UserRegistrationForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, PremiumUser
 

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email', 'username', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    USER_TYPES_CHOICES = [
        ('Normal user', 'Normal user'),
        ('Expert user', 'Expert user')]
    user_type = forms.ChoiceField(
        label="Type of user", 
        choices=USER_TYPES_CHOICES,)
    
    class Meta:
        model = Profile
        fields = ('user_type',)


class PremiumUserForm(forms.ModelForm):
    PAID_CHOICES = [('Yes', 'Yes')]
    # PAID_CHOICES = [('Yes', 'Yes'),('No', 'No')]
    paid = forms.ChoiceField(label="Get premium?", choices=PAID_CHOICES)

    class Meta:
        model = PremiumUser
        fields = ('paid',)