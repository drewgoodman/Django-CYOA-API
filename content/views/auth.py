from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from ..forms import UserLoginForm
from ..models import Campaign

# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return redirect("/login")
    queryset = Campaign.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'content/home.html', context)


def login_view(request):
    title = "Login"
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request, "Welcome, %s, you are successfully logged in." % (username))
        if next: # if prompted to login, will redirect back to the intended page
            return redirect(next)
        return redirect("/")
    context = {
        "form": form,
        "title": title,
    }
    return render(request, "content/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    return redirect("/")