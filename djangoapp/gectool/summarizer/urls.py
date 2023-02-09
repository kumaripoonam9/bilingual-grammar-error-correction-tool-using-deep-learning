from django.urls import path
from . import views

urlpatterns = [
    path('', views.summarizer, name='summarizer'),
    path('views', views.upload_driver, name="summarizer/views"),
]