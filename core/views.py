from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.functions import get_tag_list, get_question_list, save_and_authenticate_user
from core.models import Question
from core.forms import QuestionForm


def home(request):
    if request.user.is_authenticated:
        tag_list = get_tag_list(request)
        question_list = get_question_list(request)

        return render(request, "home.html", {"tag_list": tag_list, "question_list": question_list})

    else:  # if not request.user.is_authenticated
        if request.method == "POST":
            if UserCreationForm(request.POST).is_valid():
                save_and_authenticate_user(request)
                return redirect("home")
            else:
                user_creation_form = UserCreationForm(request.POST)
                return render(request, 'signup.html', {'user_creation_form': user_creation_form})

        else:  # if not request.method == "POST"
            user_creation_form = UserCreationForm()
            return render(request, 'signup.html', {'user_creation_form': user_creation_form})


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'login.html')


@login_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

            return redirect('home')
    else:
        return render(request, 'CRUDquestion/create_question.html')


@login_required
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if question.user == request.user:
        question.delete()

    return redirect('home')


@login_required
def edit_question(request, question_id):
    question = Question.objects.get(id=question_id)
    user = request.user

    if question.user == user:

        if request.method == 'POST':
            question.q = request.POST.get('q')
            question.a = request.POST.get('a')
            question.tag = request.POST.get('tag')

            question.save()

            return redirect('home')

        else:
            return render(request, 'CRUDquestion/edit_question.html', {'question': question})

    else:
        return redirect('home')


@login_required
def search_question(request):
    user = request.user
    query = request.GET.get('q')

    question_list = Question.objects.filter(q__icontains=query, user=user)
    tag_list = Question.objects.filter(user=user).order_by().values('tag').distinct()

    return render(request, 'search.html', {"question_list": question_list, "query": query, "tag_list": tag_list})


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
