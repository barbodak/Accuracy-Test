from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import AcuTest, QuizInfo


class AcuTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcuTest
        fields = 'answer'

    def update(self, instance, validated_data):
        instance.answer = validated_data.get('answer', instance.Answer)
        instance.save()
        return instance
