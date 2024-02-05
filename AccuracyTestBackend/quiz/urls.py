from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('start-quiz/<str:quiz_type>/',
         views.QuizViewSet.as_view({'post': 'startQuiz'})),
]
