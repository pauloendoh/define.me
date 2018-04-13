from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login

from core.models import Question


def create_user_by_form(post_data):
    user_creation_form = UserCreationForm(post_data)
    if user_creation_form.is_valid():
        user_creation_form.save()
        return True
    return False


def create_question_by_ajax():
    # if request.method == 'POST':
    #    question_id = request.POST.get("id")
    #    answer = request.POST.get('a')
    #    question = Question.objects.get(id=question_id)
    #    question.a = answer
    #    question.save()
    pass


def get_tag_list(request):
    user = request.user
    tag_list = Question.objects.filter(user=user).order_by().values('tag').distinct()

    return tag_list


def get_question_list(request):
    user = request.user

    if request.GET.get('tag'):
        active_tag = request.GET.get('tag')
        question_list = Question.objects.filter(user=user, tag=active_tag).order_by('-updated_at')

    else:
        question_list = Question.objects.filter(user=user).order_by('-updated_at')

    return question_list


def save_and_authenticate_user(request):
    user_creation_form = UserCreationForm(request.POST)
    user_creation_form.save()

    username = user_creation_form.cleaned_data.get('username')
    raw_password = user_creation_form.cleaned_data.get('password1')

    user = authenticate(username=username, password=raw_password)
    auth_login(request, user)

    return
