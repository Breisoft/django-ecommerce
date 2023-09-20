from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer

from common.base import UserOwnedModelViewSet

class AccountViewSet(UserOwnedModelViewSet):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()