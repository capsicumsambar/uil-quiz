# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("start/", views.start_quiz, name="start_quiz"),
    path("question/", views.quiz_question, name="quiz_question"),
    path("check-answer/", views.check_answer, name="check_answer"),
    path("next/", views.next_question, name="next_question"),
    path("results/", views.results, name="results"),
    path("spelling/", views.spelling_bee, name="spelling_bee"),
]
