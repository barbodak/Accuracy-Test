from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AcuTest, QuizInfo, ValuTest


class AcuTestSerializer(serializers.ModelSerializer):
    quiz_info = serializers.SlugRelatedField(
        read_only=True, slug_field='start_time')

    class Meta:
        model = AcuTest
        fields = ['answers', 'quiz_info']


class ValuTestSerializer(serializers.ModelSerializer):
    quiz_info = serializers.SlugRelatedField(
        read_only=True, slug_field='start_time')

    class Meta:
        model = ValuTest
        fields = ['answers', 'quiz_info']
