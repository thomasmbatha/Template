from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import User


# Create your views here.

# View to handle user login
def login_view(request):
    validation_error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            validation_error = "Invalid username and/or password."
    
    return render(request, "accounts/login.html", {
        "validation_error": validation_error,
    })


# View to handle user logout
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return HttpResponseRedirect(reverse("index"))

# View to handle user registration
def register(request):
    username_error = None
    password_error = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        
        # Check if password and confirmation match
        if password != confirmation:
            password_error = "Passwords must match."
        else:
            try:
                # Create a new user
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                messages.success(request, "Registration successful.")
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError:
                username_error = "Username already exists."
    
    return render(request, "accounts/register.html", {
        "username_error": username_error,
        "password_error": password_error,
    })
