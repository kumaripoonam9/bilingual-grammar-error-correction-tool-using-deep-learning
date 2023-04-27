from django.urls import path
from . import views

urlpatterns = [
    path('chat', views.chat, name='chat'),
    path('', views.expert_review, name='expert_review'),
    path('<str:room_name>', views.messaging, name='room'),
    path('verification', views.verification, name='expert_verification'),
    path('<str:room_name>/edit_room_name/', views.edit_room_name, name='edit_room_name'),

]