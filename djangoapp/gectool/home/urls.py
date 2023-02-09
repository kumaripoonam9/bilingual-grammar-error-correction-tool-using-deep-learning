from django.urls import path, include
from . import views
from spellcheck.views import pdf

urlpatterns = [
    path('', views.home, name='home'),

    path('tools', views.tools, name='tools'),

    path('result/pdf', pdf, name='result/pdf'),

    # path('userauth/', include('userauth.urls')),
    
    # path('grammarcheck/', include('grammarcheck.urls')),

]