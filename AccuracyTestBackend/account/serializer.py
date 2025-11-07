from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    # --- Read-only fields for the Svelte page 'retrieve' method ---

    # Get username from the related User model
    username = serializers.CharField(source="user.username", read_only=True)

    # Get organization name from the related Organization model
    organization_name = serializers.CharField(
        source="organization.name", read_only=True
    )

    class Meta:
        model = Account
        fields = [
            # Fields for the finalize() form
            "first_name",
            "last_name",
            "age",
            "sex",
            # --- Read-only fields for Svelte ---
            "username",
            "organization_name",
            "is_final",
            "acuTest_permition",
            "valTest_permition",
        ]

        # We mark 'is_final' as read-only because views.py sets it manually
        read_only_fields = [
            "username",
            "organization_name",
            "is_final",
            "acuTest_permition",
            "valTest_permition",
        ]

        # Mark the writeable fields as 'required' for the finalize step
        # This ensures serializer.is_valid() works correctly
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "age": {"required": True, "allow_null": False},
            "sex": {"required": True, "allow_null": False, "allow_blank": False},
        }
