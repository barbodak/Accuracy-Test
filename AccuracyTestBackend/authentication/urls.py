from django.urls import URLPattern, path
from . import views

URLPattern = [
    path('login/', views.LoginView.as_view(), name="login"),
]
