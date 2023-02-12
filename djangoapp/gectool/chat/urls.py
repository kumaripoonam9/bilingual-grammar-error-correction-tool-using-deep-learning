from django.urls import path
from . import views

urlpatterns = [
    path('', views.messages_page, name="chat"),
    path('<str:username>', views.chat_page, name="chat"),
]