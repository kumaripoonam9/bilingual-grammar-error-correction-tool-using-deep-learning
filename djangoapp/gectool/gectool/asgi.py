"""
ASGI config for gectool project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from chat.consumers import PersonalChatConsumer



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gectool.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('chat/ws/<int:id>/', PersonalChatConsumer.as_asgi()),
        ])
    )
})
