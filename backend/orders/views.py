from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemCreateSerializer

class CartDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response(
                {"error":"Cart not found"},
                status = status.HTTP_404_NOT_FOUND
            )
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartAPIView(APIView):
    def post(self, request, cart_id):
        serializer = CartItemCreateSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            return Response(
                {"error":"Cart not found"},
                status = status.HTTP_404_NOT_FOUND
            )

        try:
            product = Product.objects.get(
                pk=product_id,
                is_active = True
            )
            
        except  Product.DoesNotExist:
            return Response(
                {"error":"Product not found"},
                status = status.HTTP_404_NOT_FOUND
            )

        if quantity > product.stock:
            return Response(
                {"error": "Not Enough Stock"},
                status = status.HTTP_400_BAD_REQUEST
            )

        cart_item, created = CartItem.objects.get_or_create(
            cart = cart,
            product = product,
            defaults = {'quantity': quantity}
        )

        if not created:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"error" : "Not enough stock"},
                    status = status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(
            {
                "message":"Product added to cart",
                "cart_item_id":cart_item.id,
                "product": product.name,
                "quantity": cart_item.quantity
            },
            status = status.HTTP_201_CREATED
        )
            
class CartItemUpdateAPIView(APIView):
    def patch(self, request, pk):
        serializer = CartItemUpdateSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(
                serializer.error,
                status = status.HTTP_400_BAD_REQUEST
            )
        quantity = serializer.validated_data['quantity']

        try:
            cart_item =  CartItem.objects.get(pk=pk)
        except CartItem.DoesNootExist:
            return Response(
                {"error":"Cart Item Not found"},
                status = status.HTTP_404_NOT_FOUND
            )       

        product = cart_item.product

        if quantity > product.stock:
            return Response(
                {"error":"Not enough stock"},
                status = status.HTTP_400_BAD_REQUEST
            )
        cart_item.quantity = quantity 
        cart_item.save()

        return Response(
            {
                "message":"Cart quantity updated",
                "cart_item_id" cart_item.id,
                "product":product.name,
                "quantity": cart_item.quantity
            },
            status=status.HTTP_200_OK
        )