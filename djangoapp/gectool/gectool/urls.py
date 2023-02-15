from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('home.urls')),
    
    path('userauth/', include('userauth.urls')),
    
    path('grammarcheck/', include('grammarcheck.urls')),
    
    path('spellcheck/', include('spellcheck.urls')),
    
    path('summarizer/', include('summarizer.urls')),

    path('expert/', include('expert.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)