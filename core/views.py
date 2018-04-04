from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.models import Question
from core.forms import CreateQuestionForm


def home(request):
    user = request.user

    if user.is_authenticated:

        question_list = Question.objects.filter(user=user).order_by('-updated_at')
        tag_list = Question.objects.filter(user=user).order_by().values('tag').distinct()

        return render(request, 'home.html', {"question_list": question_list, "tag_list": tag_list})

    else:
        user_creation_form = UserCreationForm()

        if request.method == 'POST':
            user_creation_form = UserCreationForm(request.POST)

            if user_creation_form.is_valid():
                user_creation_form.save()

                username = user_creation_form.cleaned_data.get('username')
                raw_password = user_creation_form.cleaned_data.get('password1')

                user = authenticate(username=username, password=raw_password)
                auth_login(request, user)

                return redirect('home')

        return render(request, 'signup.html', {'user_creation_form': user_creation_form})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
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
            return redirect('home')
    return render(request, 'create_question.html')


@login_required
def delete_question(request):
    if request.method == 'POST':
        question_id = request.POST.get("id")
        question = Question.objects.get(id=question_id)
        if question.user == request.user:
            question.delete()
    return redirect('home')


@login_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    user = User.objects.get(id=request.user.id)
    if question.user == user:
        if request.method == 'POST':
            question.q = request.POST.get('q')
            question.a = request.POST.get('a')
            question.tag = request.POST.get('tag')
            question.save()
            return redirect('home')
        return render(request, 'edit_question.html', {'question': question})
    else:
        return redirect('home')


@login_required
def search_question(request):
    user = request.user
    query = request.GET.get('q')
    results = Question.objects.filter(q__icontains=query, user=user)
    tags = Question.objects.filter(user=user).order_by().values('tag').distinct()
    return render(request, 'search.html', {"results": results, "query": query, "tags": tags})


@login_required
def show_tag(request, tag):
    user = request.user
    questions = Question.objects.filter(user=user, tag=tag).order_by('-updated_at')
    tags = Question.objects.filter(user=user).order_by().values('tag').distinct()

    return render(request, 'tag.html', {"tag": tag, "questions": questions, "tags": tags, "tag_name": tag})


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
