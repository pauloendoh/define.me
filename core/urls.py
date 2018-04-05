from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/login'}, name='logout'),
    path('create/', views.create_question, name='create_question'),
    path('delete/<int:question_id>', views.delete_question, name='delete_question'),
    path('edit/<int:question_id>', views.edit_question, name='edit_question'),
    path('search', views.search_question, name='search_question'),
    path('ajax/update_question', views.update_question, name='update_question')
]
