# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, Address
from .serializers import UserSerializer, AddressSerializer

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)

class UserDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status = status.HTTP_404_NOT_FOUND
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)

class AddressListAPIView(APIView):
    def get(self, request):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many = True)
        return Response(serializer.data)

class AddressDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response(
                {"error": "Address not found"},
                status = status.HTTP_404_NOT_FOUND
            )

        serializer = AddressSerializer(address)
        return Response(serializer.data)