from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()


def messages_page(request):
    users = User.objects.exclude(username=request.user.username)
    context = {'users':users}

    return render(request, "chat/messages.html", context)

# def detail(request, pk):
#     context = {}
#     return render(request, "chat/messages.html", context)

def chat_page(request, username):
    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    context = {
        'users': users,
        'user': user_obj
    }

    return render(request, "chat/messages.html", context)