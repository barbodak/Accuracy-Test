from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('start-quiz/<str:quiz_type>/',
         views.QuizViewSet.as_view({'post': 'startQuiz'})),
    path('submit-answer/<str:quiz_type>/',
         views.QuizViewSet.as_view({'put': 'submitAnswer'})),
    path('retrieve/<str:quiz_type>/',
         views.QuizViewSet.as_view({'get': 'retrieve'})),
    path('has-quiz-ended/<str:quiz_type>/',
         views.QuizViewSet.as_view({'get': 'hasQuizEnded'})),
]
