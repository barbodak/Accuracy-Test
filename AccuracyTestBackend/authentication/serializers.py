from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['username']
