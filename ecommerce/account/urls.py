from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

from django.urls import path, include


router = DefaultRouter()
router.register(r'', views.AccountViewSet, basename='account')

urlpatterns = [
    path('', include(router.urls)),
]
