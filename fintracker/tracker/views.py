from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm  # We'll define this form in the next step
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Register View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        else:
            messages.error(request, "Error during registration. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, "Invalid login credentials.")
        else:
            messages.error(request, "Invalid login credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'tracker/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('login')  # Redirect to the login page after logout


# Dashboard View (Only accessible after login)
@login_required
def dashboard(request):
    return render(request, 'tracker/dashboard.html')