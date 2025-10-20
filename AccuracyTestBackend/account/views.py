from django.shortcuts import render
from rest_framework import viewsets, status
from datetime import timedelta
from warnings import warn
from django.contrib.auth.models import User
from django.db.models import query
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication

from .serializer import AccountSerializer
from account.models import Account
from .models import Account


class AccountViewSet(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication,)
    ermission_classes = (IsAuthenticated,)

    def retrieve(self, request):
        account = Account.objects.get(user=request.user)
        if account is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        return JsonResponse(AccountSerializer(account).data)
