from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def chat(request):
    # print(request.user.premiumuser.paid)
    # if request.user.premiumuser.paid == "Yes":
    #     return render(request, "expert/chat.html")
    # else:
    #     return render('home')
    return render(request, "expert/chat.html")