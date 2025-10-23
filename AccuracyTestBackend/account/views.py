from django.shortcuts import render
from rest_framework import viewsets, status
from django.contrib.auth.models import User
# from django.http import HttpResponse # <-- DO NOT USE
# from django.http.response import JsonResponse # <-- DO NOT USE

# --- DRF Imports ---
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .serializer import AccountSerializer
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
