from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm, ProfileForm, PremiumUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(user.profile.user_type)
            return redirect('../../')
            # if user.profile.user_type=='Normal user':
            #     return redirect('../../')
            # else:
            #     return redirect('experthome')
    else:
        form = AuthenticationForm()

    return render(request, "userauth/login.html", {'form':form})


def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            
            profile.user = user

            profile.save()

            messages.success(request, 'Account created successfully') 
            return redirect('login')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()

    context = {'form': form, 'profile_form':profile_form}
    return render(request, "userauth/register.html", context)   


@login_required(login_url='login')
def logout_request(request):
    if request.method == "POST":
        logout(request)

        return redirect('../../')


@login_required(login_url='login')
def userprofile(request):
    if request.method == "POST":
        premium_form = PremiumUserForm(request.POST)
        if premium_form.is_valid():
            paid_user = premium_form.save(commit=False)
            paid_user.user = request.user
            paid_user.save()
            return redirect('profile')
    else:
        premium_form = PremiumUserForm()
    
    context = {'premium_form':premium_form}
    return render(request, "userauth/profile.html", context)