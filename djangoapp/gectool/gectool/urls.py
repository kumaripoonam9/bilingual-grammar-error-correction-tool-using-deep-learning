from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    
    path('userauth/', include('userauth.urls')),
    
    path('grammarcheck/', include('grammarcheck.urls')),
    
    path('spellcheck/', include('spellcheck.urls')),
    
    path('summarizer/', include('summarizer.urls')),

    path('expert/', include('expert.urls')),
]