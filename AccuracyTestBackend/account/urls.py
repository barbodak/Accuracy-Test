from django.contrib.auth.models import User, Group
from rest_framework import serializers
from knox.serializers import UserSerializer
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("retrieve/", views.AccountViewSet.as_view({"get": "retrieve"})),
    path("finalize/", views.AccountViewSet.as_view({"post": "finalize"})),
]
