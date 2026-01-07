from knox.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import Account, Organization
import secrets
import string


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
            "email",
            "university",
            "major",
            "degree",
            "phone",
            # --- Read-only fields for Svelte ---
            "username",
            "organization_name",
            "is_final",
            "acuTest_permission",
            "valuTest_permission",
        ]

        # We mark 'is_final' as read-only because views.py sets it manually
        read_only_fields = [
            "username",
            "organization_name",
            "is_final",
            "acuTest_permission",
            "valuTest_permission",
        ]

        # Mark the writeable fields as 'required' for the finalize step
        # This ensures serializer.is_valid() works correctly
        extra_kwargs = {
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
            "age": {"required": True, "allow_null": False},
            "sex": {"required": True, "allow_null": False, "allow_blank": False},
        }


class SignupSerializer(serializers.Serializer):
    """Serializer for user signup that creates both User and Account with auto-generated credentials"""

    first_name = serializers.CharField(required=True, max_length=255, allow_blank=False)
    last_name = serializers.CharField(required=True, max_length=255, allow_blank=False)
    email = serializers.EmailField(required=False, allow_blank=True)
    age = serializers.IntegerField(required=False, allow_null=True)
    sex = serializers.ChoiceField(
        choices=Account.SEX_CHOICES, required=False, allow_null=True
    )
    phone = serializers.CharField(required=False, max_length=255, allow_blank=True)
    university = serializers.CharField(required=False, max_length=255, allow_blank=True)
    major = serializers.CharField(required=False, max_length=255, allow_blank=True)
    degree = serializers.ChoiceField(
        choices=Account.DEGREE_CHOICES, required=False, allow_null=True
    )

    def generate_unique_username(self, existing_usernames, length=8):
        """
        Generates a random, unique username by checking against an
        in-memory set of existing usernames.
        """
        alphabet = string.ascii_lowercase + string.digits
        while True:
            username = "user_" + "".join(
                secrets.choice(alphabet) for _ in range(length)
            )
            if username not in existing_usernames:
                return username

    def create(self, validated_data):
        """Create User and Account with auto-generated username and password"""
        # Get or create Sharif_Job_Expo organization
        organization, _ = Organization.objects.get_or_create(name="Sharif_Job_Expo")

        # Get existing usernames to avoid conflicts
        existing_usernames = set(User.objects.values_list("username", flat=True))

        # Generate unique username and password
        username = self.generate_unique_username(existing_usernames, length=8)
        password = secrets.token_urlsafe(8)

        # Create User with auto-generated credentials
        user = User.objects.create_user(
            username=username,
            password=password,
            email=validated_data.get("email", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # Create Account with valuTest_permission=True
        # The signal will automatically create the ValuTest object
        account = Account.objects.create(
            user=user,
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", ""),
            age=validated_data.get("age"),
            sex=validated_data.get("sex"),
            university=validated_data.get("university", ""),
            phone=validated_data.get("phone", ""),
            major=validated_data.get("major", ""),
            degree=validated_data.get("degree"),
            organization=organization,
            # valuTest_permission=True,  # Give permission to take value test
            acuTest_permission=True,  # Give permission to take value test
        )

        return account
