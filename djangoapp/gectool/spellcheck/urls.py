from django.urls import path
from . import views

urlpatterns = [
    path('', views.spellcheck, name='spellcheck'),
    path('pdf', views.pdf, name='spellcheck/pdf'),
    path('views', views.upload_driver, name="spellcheck/views")
]