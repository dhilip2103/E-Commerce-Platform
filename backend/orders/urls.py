from django.urls import path

from .views import (
    CartDetailAPIView, 
    AddToCartAPIView,
    CartItemUpdateAPIView,
)

urlpatterns = [

    path(
        'cart/<int:cart_id>/items/',
        AddToCartAPIView.as_view(),
        name = 'add-to-cart'
    ),


    path(
        'cart/items/<int:pk>/',
        CartItemUpdateAPIView.as_view(),
        name = 'cart-item-update'
    ),
    
    
    
    path(
        '<int:pk>/',
        CartDetailAPIView.as_view(), 
        name='cart-detail'),
]