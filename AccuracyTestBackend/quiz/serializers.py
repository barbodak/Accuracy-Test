from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AcuTest_pic, AcuTest_text, Quiztime, ValuTest


class AcuTestPicSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = AcuTest_pic
        fields = ["answers", "quiz_time"]


class AcuTestPicAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcuTest_pic
        fields = ["correct", "wrong"]


class AcuTestTextSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = AcuTest_text
        fields = ["answers", "quiz_time"]


class AcuTestTextAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcuTest_text
        fields = [
            "correct",
            "wrong",
            "num_of_no",
            "num_of_yes",
            "no_no",
            "no_yes",
            "yes_no",
            "yes_yes",
        ]


class ValuTestSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = ValuTest
        fields = ["answers", "quiz_time"]


class ValuTestAnswerSerializer(serializers.ModelSerializer):
    quiz_time = serializers.SlugRelatedField(read_only=True, slug_field="start_time")

    class Meta:
        model = ValuTest
        fields = [
            "sharayet_kari",
            "hemayat",
            "ravabet",
            "pishraft",
            "esteghlal",
            "tofigh",
            "quiz_time",
        ]
