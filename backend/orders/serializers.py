from rest_framework import serializers
from .models import Cart, CartItem

from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'quantity',
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        source = 'cartitem_set',
        many = True,
        read_only = True
    ) 
    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'items',
            'created_at',
            'updated_at',
        ]
    
class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value = 1)

class CartItemUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)

class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()

    