from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def index(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('index')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'login.html')