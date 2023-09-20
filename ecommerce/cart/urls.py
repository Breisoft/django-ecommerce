from django.urls import path
from .views import CartViewSet, CartItemViewSet

urlpatterns = [
    path('', CartViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='cart-list'),

    path('me/', CartViewSet.as_view({
        'get': 'me'
    }), name='cart-me'),

    path('<int:id>/', CartViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='cart-detail'),

    path('<int:id>/items/', CartItemViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='cart-item-list'),

    path('<int:id>/items/<int:item_id>/', CartItemViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'post': 'create',
        'delete': 'destroy'
    }), name='cart-item-detail'),

    path('<int:id>/items/clear/', CartItemViewSet.as_view({
        'delete': 'clear',
    }), name='cart-clear')
]
