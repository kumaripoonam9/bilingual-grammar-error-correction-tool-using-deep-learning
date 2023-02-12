from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES_CHOICES = [
        ('Normal user', 'Normal user'),
        ('Expert user', 'Expert user')]
    user_type = models.CharField(
        max_length=11,
        choices=USER_TYPES_CHOICES,)
    
    # friends = models.ManyToManyField('Friend', related_name='my_friends')

    def __str__(self):
        return f'{self.user.username}'


class PremiumUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PAID_CHOICES = [('Yes', 'Yes')]
    # PAID_CHOICES = [('Yes', 'Yes'),('No', 'No')]
    paid = models.CharField(max_length=3, choices=PAID_CHOICES)

    def __str__(self):
        return f'{self.user.username}'