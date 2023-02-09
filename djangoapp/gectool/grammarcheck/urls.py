from django.urls import path
from . import views

urlpatterns = [
    path('', views.grammarcheck, name='grammarcheck'),
    path('pdf', views.pdf, name='grammarcheck/pdf'),
    path('views', views.upload_driver, name="grammarcheck/views"),
]