from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AcuTest_pic, AcuTest_text, Quiztime, ValuTest


class AcuTestPicSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = AcuTest_pic
        fields = ["answers", "quiz_time"]


class AcuTestTextSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = AcuTest_text
        fields = ["answers", "quiz_time"]


class ValuTestSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = ValuTest
        fields = ["answers", "quiz_time"]
