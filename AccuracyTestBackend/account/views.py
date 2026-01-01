from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from django.contrib.auth.models import User
from django.contrib.auth import login
# from django.http import HttpResponse # <-- DO NOT USE
# from django.http.response import JsonResponse # <-- DO NOT USE

# --- DRF Imports ---
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from knox.models import AuthToken

from .serializer import AccountSerializer, SignupSerializer
from .models import Account
import logging


class AccountViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)  # <-- FIXED TYPO

    def retrieve(self, request):
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            # Use DRF's Response
            return Response(
                {"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = AccountSerializer(account)
        # Use DRF's Response
        return Response(serializer.data, status=status.HTTP_200_OK)

    def finalize(self, request):
        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            # Use DRF's Response
            return Response(
                {"error": "Account not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if account.is_final:
            # Use DRF's Response
            return Response(
                {"error": "Account is already finalized"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use the serializer to validate the incoming data (request.data)
        serializer = AccountSerializer(account, data=request.data, partial=True)

        if serializer.is_valid():
            # This logic is correct: save serializer, then save account
            serializer.save()

            account.is_final = True
            account.save()

            # Re-serialize the *full* account object to send back
            response_serializer = AccountSerializer(account)

            # Use DRF's Response
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        else:
            # Use DRF's Response to return the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(APIView):
    """View for user signup that creates User, Account, and returns authentication token"""

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = SignupSerializer(data=request.data)
        logger = logging.getLogger(__name__)
        logger.warning(request.data)

        if serializer.is_valid():
            account = serializer.save()

            login(request, account.user)

            token = AuthToken.objects.create(account.user)[1]

            return Response(
                {"token": token, "account": AccountSerializer(account).data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
