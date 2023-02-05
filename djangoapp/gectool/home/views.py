from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "home/home.html")

# def experthome(request):
#     return render(request, "home/experthome.html")

# def login(request):
#     return render(request, "home/login.html")

# def register(request):
    # return render(request, "home/register.html")

def tools(request):
    return render(request, "home/tools.html")