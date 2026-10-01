from django.urls import path

from .views import (
    CartDetailAPIView, 
    AddToCartAPIView,
    CartItemUpdateAPIView,
    CheckoutAPIView,
)

urlpatterns = [

    path(
        'cart/<int:cart_id>/items/',
        AddToCartAPIView.as_view(),
        name = 'add-to-cart'
    ),

    path(
        'cart/<int:cart_id>/checkout/',
        CheckoutAPIView.as_view(),
        name='checkout'
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