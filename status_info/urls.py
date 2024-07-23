from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.stats_page, name='stats_page'),
    path('skill_<str:skill_name>', views.skill_detail, name='skill_detail'),
    path('job_<str:job_name>', views.job_detail, name='job_detail'),
    path('title_<str:title_name>', views.title_detail, name='title_detail'),
    path('quests', views.quests_page, name='quests_page'),
    path('add_new_quest', views.create_quest, name='create_quest'),
    path('quest_completion_post', views.quest_completion_post, name='quest_completion_post'),
    path('reflection', views.reflection_page, name='reflection_page'),
    path('add_new_reflection', views.create_reflection, name='create_reflection'),
    path('reflection_post', views.reflection_post, name='reflection_post'),
    path('sign_up', views.signup, name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='status_info/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout_page', views.logout_page, name='logout_page'),

]

