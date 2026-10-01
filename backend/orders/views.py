from django.shortcuts import render

# Create your views here.
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem, Order, OrderItem

from users.models import Address

from products.models import Product
from .serializers import (
    CartSerializer, 
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CheckoutSerializer,
)

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

        serializer = CartItemUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        quantity = serializer.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product = cart_item.product

        if quantity > product.stock:
            return Response(
                {"error": "Not enough stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            {
                "message": "Cart quantity updated",
                "cart_item_id": cart_item.id,
                "product": product.name,
                "quantity": cart_item.quantity
            },
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):

        try:
            cart_item = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response(
                {"error": "Cart item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        product_name = cart_item.product.name

        cart_item.delete()

        return Response(
            {
                "message": "Product removed from cart",
                "product": product_name
            },
            status=status.HTTP_200_OK
        )

class CheckoutAPIView(APIView):

    def post(self, request, cart_id):

        serializer = CheckoutSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        address_id = serializer.validated_data['address_id']

        try:
            cart = Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            return Response(
                {"error": "Cart not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            address = Address.objects.get(
                pk=address_id,
                user=cart.user
            )
        except Address.DoesNotExist:
            return Response(
                {"error": "Address not found for this user"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total_amount = 0

        for cart_item in cart_items:

            product = cart_item.product

            if cart_item.quantity > product.stock:
                return Response(
                    {
                        "error": f"Not enough stock for {product.name}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_amount += product.price * cart_item.quantity

        with transaction.atomic():

            order = Order.objects.create(
                user=cart.user,
                address=address,
                total_amount=total_amount,
                status='PENDING'
            )

            for cart_item in cart_items:

                product = cart_item.product

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item.quantity,
                    price=product.price
                )

                product.stock -= cart_item.quantity
                product.save()

            cart_items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_amount": str(order.total_amount),
                "status": order.status
            },
            status=status.HTTP_201_CREATED
        )
