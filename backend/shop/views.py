# Create your views here.

from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Sweet
from .serializers import RegisterSerializer, SweetSerializer
from .permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import CustomTokenObtainPairSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import parser_classes





# ===============================
# AUTHENTICATION API
# ===============================

# This API handles user login
# Method: POST
# Access: Public
# Purpose: Returns JWT access and refresh tokens

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



# This API registers a new user
# Method: POST
# Access: Public
# Purpose: Create a new user account
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ===============================
# USER APIs (Customer Side)
# ===============================

# This API lists all available sweets
# Method: GET
# Access: Logged-in Users
# Purpose: View all sweets in the shop

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_sweets(request):
    sweets = Sweet.objects.all()
    serializer = SweetSerializer(sweets, many=True)
    return Response(serializer.data)


# This API allows a user to purchase a sweet
# Method: POST
# Access: Logged-in Users
# Purpose: Reduce sweet quantity by 1 after purchase
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def purchase_sweet(request, pk):
    try:
        sweet = Sweet.objects.get(pk=pk)
    except Sweet.DoesNotExist:
        return Response({'error': 'Sweet not found'}, status=404)

    if sweet.quantity == 0:
        return Response({'error': 'Out of stock'}, status=400)

    sweet.quantity -= 1
    sweet.save()
    return Response({'message': 'Sweet purchased'}, status=200)


# This API searches sweets based on filters
# Method: GET
# Access: Logged-in Users
# Purpose: Search by name, category, or price range

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def search_sweets(request):
    sweets = Sweet.objects.all()

    name = request.GET.get('name')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if name:
        sweets = sweets.filter(name__icontains=name)

    if category:
        sweets = sweets.filter(category__icontains=category)

    if min_price:
        sweets = sweets.filter(price__gte=min_price)

    if max_price:
        sweets = sweets.filter(price__lte=max_price)

    serializer = SweetSerializer(sweets, many=True)
    return Response(serializer.data)





# ===============================
# ADMIN APIs (Shop Owner / Admin)
# ===============================

# This API adds a new sweet to the shop
# Method: POST
# Access: Admin Only
# Purpose: Create a new sweet with image support


@api_view(["POST"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])

def create_sweet(request):
    serializer = SweetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# This API updates existing sweet details
# Method: PUT
# Access: Admin Only
# Purpose: Edit price, quantity, name, or image

@api_view(["PUT"])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def update_sweet(request, pk):
    try:
        sweet = Sweet.objects.get(pk=pk)
    except Sweet.DoesNotExist:
        return Response({"error": "Sweet not found"}, status=404)

    serializer = SweetSerializer(sweet, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)



# This API deletes a sweet from the system
# Method: DELETE
# Access: Admin Only
# Purpose: Remove sweet permanently

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def delete_sweet(request, pk):
    try:
        Sweet.objects.get(pk=pk).delete()
        return Response(status=204)
    except Sweet.DoesNotExist:
        return Response({'error': 'Sweet not found'}, status=404)




# This API increases the stock quantity of a sweet
# Method: POST
# Access: Admin Only
# Purpose: Add more stock to an existing sweet

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def restock_sweet(request, pk):
    try:
        sweet = Sweet.objects.get(pk=pk)
    except Sweet.DoesNotExist:
        return Response({'error': 'Sweet not found'}, status=404)

    quantity = int(request.data.get('quantity', 0))
    sweet.quantity += quantity
    sweet.save()

    return Response({'message': 'Sweet restocked'}, status=200)







