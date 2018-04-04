from django.contrib.auth.forms import UserCreationForm

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

