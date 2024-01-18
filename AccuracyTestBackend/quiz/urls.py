from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('start_quiz/', views.startQuiz),
]
