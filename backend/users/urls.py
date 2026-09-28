from django.urls import path
from .views import (
    UserListAPIView, 
    UserDetailAPIView,
    AddressListAPIView,
    AddressDetailAPIView,
)

urlpatterns = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),

    path('addresses/', AddressListAPIView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailAPIView.as_view(), name='address-detail'),
]