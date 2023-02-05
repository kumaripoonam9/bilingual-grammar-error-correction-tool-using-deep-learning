from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('tools', views.tools, name='tools'),

    path('userauth/', include('userauth.urls')),
    
    path('grammarcheck/', include('grammarcheck.urls')),

    path('chat', include('expert.urls')),
]