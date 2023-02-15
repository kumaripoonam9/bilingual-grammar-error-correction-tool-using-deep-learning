from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('', views.expert_review, name='expert_review'),
    path('chat/<str:room_name>', views.messaging, name='room'),
    path('verification', views.verification, name='expert_verification'),
]