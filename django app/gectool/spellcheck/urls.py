from django.urls import path
from . import views

urlpatterns = [
    path('', views.spellcheck, name='spellcheck'),
]