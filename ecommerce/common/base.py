from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ModelViewSet

class UserOwnedModelViewSet(ModelViewSet):
    """
    Abstract viewset that filters the queryset to return only objects owned by the authenticated user.
    Returns 404 if the resource is not found or if the user doesn't have permission to access it.
    """
    user_field = 'user'
    serializer_class = None 

    def list(self, request, *args, **kwargs):
        raise NotFound("Endpoint not available.")

    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        return super().get_queryset().filter(**{self.user_field: user})


    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # Get the object associated with the current user.
        obj = self.queryset.model.objects.get(**{self.user_field: request.user})
        serializer = self.serializer_class(obj)
        return Response(serializer.data)