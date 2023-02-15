from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name 
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return str(self.room)
    
class ExpertLanguage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LANGUAGES = [
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Both hindi and english', 'Both hindi and english')
    ]
    languages_known = models.CharField(max_length=255, choices=LANGUAGES)
    cerificates = models.FileField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'
    

class PendingExpertReview(models.Model):
    expert = models.ForeignKey(User, on_delete=models.CASCADE)
    pending_room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pending_room)
