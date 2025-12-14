from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CustomTokenObtainPairView



from .views import (
    RegisterView, list_sweets, purchase_sweet,
    create_sweet, search_sweets, update_sweet, delete_sweet, restock_sweet
)

# This file defines all the API links (URLs) of the application
# Each URL connects a request to a specific action


urlpatterns = [
    # Auth Url

    # Register a new user (Sign Up)
    # Example: Create a new account
    path('auth/register/', RegisterView.as_view()),
    
    # Login for existing users
    # Returns a secure token after successful login
    path('auth/login/', CustomTokenObtainPairView.as_view()),
    
    # User API 
    
    # View all available sweets
    path('sweets/', list_sweets),

    # Purchase a specific sweet using its ID
    # Example: Buy sweet with ID = 3
    path('sweets/<int:pk>/purchase/', purchase_sweet),
    
    # Search sweets by name or category or price
    path('sweets/search/', search_sweets),

    # Admin API

    # Add a new sweet to the shop
    path('admin/sweets/', create_sweet),

    # Update details of a sweet (price, quantity, etc.)
    path('admin/sweets/<int:pk>/', update_sweet),

    # Delete a sweet from the system
    path('admin/sweets/<int:pk>/delete/', delete_sweet),

    # Increase stock quantity for a sweet
    path('admin/sweets/<int:pk>/restock/', restock_sweet),
]
