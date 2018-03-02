from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
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
                auth_login(request, user)
                return redirect('index')
        else:
            form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        question_id = request.POST.get("id")
        answer = request.POST.get('a')
        question = Question.objects.get(id=question_id)
        question.a = answer
        question.save()

    questions = Question.objects.filter(user=user)
    return render(request, 'home.html', {"questions": questions})


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
    return render(request, 'create_question.html', {"form": form})


@login_required
def delete_question(request):
    if request.method == 'POST':
        question_id = request.POST.get("id")
        question = Question.objects.get(id=question_id)
        if question.user == request.user:
            question.delete()
    return redirect('index')


@login_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    user = User.objects.get(id=request.user.id)
    if question.user == user:
        if request.method == 'POST':
            question.q = request.POST.get('q')
            question.a = request.POST.get('a')
            question.tag = request.POST.get('tag')
            question.priority = request.POST.get('priority')
            question.save()
            return redirect('index')
        return render(request, 'edit_question.html', {'question': question})
    else:
        return redirect('index')


@login_required
def search_question(request):
    user = request.user
    query = request.GET.get('q')
    results = Question.objects.filter(q__icontains=query, user=user)
    return render(request, 'search.html', {"results": results})


@login_required
def show_tag(request, tag):
    user = request.user
    questions = Question.objects.filter(user=user, tag=tag)
    return render(request, 'tag.html', {"tag": tag, "questions": questions})


@login_required
def update_question(request):

    data = {
        'teste': 'Testando123'
    }

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        question_q = request.POST.get('question_q')
        print("--------------------ATÉ AQUI TÁ FUNCIONANDO-----", "-------HAHAHAH")
        print(question_q)

        question = Question.objects.get(id=question_id)
        question.q = question_q
        question.save()
        print("--------------------AQUI TAMBÉM KK-----")
    return JsonResponse(data)