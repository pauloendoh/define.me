from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from core.models import Question
from .forms import CreateQuestionForm


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
    user = User.objects.get(id=request.user.id)

    if request.method =='POST':
        question_id = request.POST.get("id")
        answer = request.POST.get('a')
        question = Question.objects.get(id=question_id)
        question.a = answer
        question.save()

    questions = Question.objects.filter(user=user)
    return render(request, 'home.html', {"questions":questions})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'login.html')

@login_required
def create_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('index')
    form = CreateQuestionForm()
    return render(request, 'create_question.html', {"form":form})

@login_required
def delete_question(request):
    if request.method == 'POST':
        question_id = request.POST.get("id")
        question = Question.objects.get(id=question_id)
        if question.user == request.user :
            question.delete()
    return redirect('index')