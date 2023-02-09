from django.urls import path
from . import views

urlpatterns = [
    path('', views.spellcheck, name='spellcheck'),

    path('../result/pdf', views.pdf, name='result/pdf'),

    path('views', views.upload_driver, name="spellcheck/views")
]