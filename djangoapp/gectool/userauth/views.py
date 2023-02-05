from django.shortcuts import render, redirect
# from django.contrib.auth.forms import SignUpForm
from .forms import SignUpForm
# import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('../../')
    else:
        form = AuthenticationForm()
    # return render(request, 'login.html', {'form':form})
    return render(request, "userauth/login.html", {'form':form})


def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user.refresh_from_db()  

            # # load the profile instance created by the signal
            user.save()
            # raw_password = form.cleaned_data.get('password1')

            # # login user after signing up
            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)
            messages.success(request, 'Account created successfully') 
            return redirect('login')
    else:
        form = SignUpForm()

    return render(request, "userauth/register.html", {'form': form})   

def logout_request(request):
    if request.method == "POST":
        logout(request)
        # form = AuthenticationForm(data=request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     login(request, user)
        return redirect('../../')
    # else:
    #     form = AuthenticationForm()
    # # return render(request, 'login.html', {'form':form})
    # return render(request, "userauth/login.html", {'form':form})