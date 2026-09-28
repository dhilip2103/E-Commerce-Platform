from django.urls import path
from .views import (
    ProductListAPIView, 
    ProductDetailAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name = 'category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name = 'category-detail'),

    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),    
    

]