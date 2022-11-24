from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('register', views.register, name='register'),
    # path('login', views.login, name='login'),
    path('tools', views.tools, name='tools'),

    path('userauth/', include('userauth.urls')),
    
    path('grammarcheck/', include('grammarcheck.urls')),
]