from django.urls import path
from .views import CartDetailAPIView, AddToCartAPIView

urlpatterns = [
    path(
        'cart/<int:cart_id>/items/',
        AddToCartAPIView.as_view(),
        name = 'add-to-cart'
    ),
    
    
    
    path(
        '<int:pk>/',
        CartDetailAPIView.as_view(), 
        name='cart-detail'),
]