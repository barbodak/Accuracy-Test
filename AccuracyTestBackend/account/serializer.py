from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'acuTest_permition', 'valTest_permition', 'age', 'sex', 'organization']
