from django.contrib.auth import login
from django.contrib.auth.models import User, Group

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from knox.settings import knox_settings

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


