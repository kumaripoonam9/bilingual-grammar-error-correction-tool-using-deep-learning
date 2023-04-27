from django.db import models
from django.contrib.auth.models import User




class Room(models.Model):
    room_name = models.CharField(max_length=255)
    user_room_name = models.CharField(max_length=255, null=True, blank=True)
    expert_room_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.room_name 
    
    # def edit_room_name(self, edited_room_name, user_profile):
    #     if user_profile == "Expert user":
    #         self.expert_room_name = edited_room_name
    #     else:
    #         self.user_room_name = edited_room_name
    #     self.save()

    #     return self.room_name 




class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)
    # has_attachment = models.BooleanField(default=False)
    attachment = models.FileField(null=True, blank=True, upload_to='chat/')

    def __str__(self):
        return f'[{self.room.room_name}] {self.message}'
    



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
