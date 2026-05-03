from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from account.models import Account


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ["username"]

        from rest_framework import serializers


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username or Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = None

            # Check if input looks like an email
            if "@" in username:
                try:
                    account = Account.objects.get(email=username)
                    # Authenticate using the username of the linked user
                    user = authenticate(
                        request=self.context.get("request"),
                        username=account.user.username,
                        password=password,
                    )
                except Account.DoesNotExist:
                    pass

            # If not an email or not found, try normal username authentication
            if not user:
                user = authenticate(
                    request=self.context.get("request"),
                    username=username,
                    password=password,
                )

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
