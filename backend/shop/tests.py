from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from shop.models import Sweet


# =========================================
# COMMON JWT HELPER CLASS
# =========================================

# This class contains helper methods for JWT authentication
# It is used to get and attach login tokens during testing


class JWTTestBase(APITestCase):

    def get_jwt_token(self, username, password):
        response = self.client.post(
            "/api/auth/login/",
            {"username": username, "password": password},
            format="json"
        )
        self.assertEqual(response.status_code, 200)
        return response.data["access"]
    
    # This method attaches the JWT token to API requests
    # Purpose: Authenticate requests as a logged-in user

    def authenticate(self, token):
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )


# =========================================
# ADMIN SWEET MANAGEMENT TESTS
# =========================================

# These tests check all Admin-only sweet operations
# Includes create, update, delete, and restock


class AdminSweetTests(APITestCase):

    # This runs before each test
    # Purpose: Create an admin user and a sample sweet

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True
        )
        self.client.force_authenticate(user=self.admin)

        self.sweet = Sweet.objects.create(
            name="Barfi",
            category="Milk",
            price=100,
            quantity=10
        )

    # Test: Admin can create a new sweet

    def test_admin_create_sweet(self):
        data = {
            "name": "Chocolate",
            "category": "Candy",
            "price": 30,
            "quantity": 20
        }
        response = self.client.post("/api/admin/sweets/", data)
        self.assertEqual(response.status_code, 201)
    
    
    # Test: Admin can update sweet details

    def test_admin_update_sweet(self):
        data = {
            "name": "Barfi",
            "category": "Milk",
            "price": 120,
            "quantity": 10
        }
        response = self.client.put(
            f"/api/admin/sweets/{self.sweet.id}/", data
        )
        self.assertEqual(response.status_code, 200)

    # Test: Admin can delete a sweet
    def test_admin_delete_sweet(self):
        response = self.client.delete(
            f"/api/admin/sweets/{self.sweet.id}/delete/"
        )
        self.assertEqual(response.status_code, 204)

    
    # Test: Admin can increase sweet stock quantity
    def test_admin_restock_sweet(self):
        response = self.client.post(
            f"/api/admin/sweets/{self.sweet.id}/restock/",
            {"quantity": 5}
        )
        self.assertEqual(response.status_code, 200)




# =========================================
# AUTHENTICATION TESTS
# =========================================

# These tests check user registration and login functionality


class AuthTests(APITestCase):
    
    # Test: New user registration
    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password": "testpass123"
        }
        response = self.client.post("/api/auth/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())
    
    # Test: User login and token generation

    def test_user_login(self):
        User.objects.create_user(username="loginuser", password="loginpass")
        data = {
            "username": "loginuser",
            "password": "loginpass"
        }
        response = self.client.post("/api/auth/login/", data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)



# =========================================
# USER SWEET PURCHASE TESTS
# =========================================

class UserSweetTests(APITestCase):

    # Setup a normal user and a sweet

    def setUp(self):
        self.user = User.objects.create_user(
            username="user",
            password="userpass"
        )
        self.client.force_authenticate(user=self.user)

        self.sweet = Sweet.objects.create(
            name="Laddu",
            category="Indian",
            price=50,
            quantity=5
        )
    
    # Test: User can view all sweets

    def test_list_sweets(self):
        response = self.client.get("/api/sweets/")
        self.assertEqual(response.status_code, 200)

    # Test: User can purchase a sweet
    def test_purchase_sweet(self):
        response = self.client.post(
            f"/api/sweets/{self.sweet.id}/purchase/"
        )
        self.assertEqual(response.status_code, 200)

    # Test: User cannot purchase when stock is zero
    def test_purchase_out_of_stock(self):
        self.sweet.quantity = 0
        self.sweet.save()

        response = self.client.post(
            f"/api/sweets/{self.sweet.id}/purchase/"
        )
        self.assertEqual(response.status_code, 400)


# =========================================
# SWEET SEARCH & FILTER TESTS
# =========================================

# These tests verify search and filter functionality
# Based on name, category, and price

class SweetSearchTests(APITestCase):

    # Setup user and sample sweets
    def setUp(self):
        self.user = User.objects.create_user(
            username="searchuser",
            password="searchpass"
        )
        self.client.force_authenticate(user=self.user)

        Sweet.objects.create(
            name="Laddu",
            category="Indian",
            price=50,
            quantity=10
        )
        Sweet.objects.create(
            name="Chocolate Bar",
            category="Candy",
            price=100,
            quantity=5
        )
    
    # Test: Search sweet by name

    def test_search_by_name(self):
        response = self.client.get("/api/sweets/search/?name=laddu")
        self.assertEqual(len(response.data), 1)

    # Test: Filter sweets by category

    def test_filter_by_category(self):
        response = self.client.get("/api/sweets/search/?category=Candy")
        self.assertEqual(len(response.data), 1)

    # Test: Filter sweets by price range
    def test_filter_by_price_range(self):
        response = self.client.get("/api/sweets/search/?min_price=60")
        self.assertEqual(len(response.data), 1)
