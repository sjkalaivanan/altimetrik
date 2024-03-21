from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.urls import reverse
from .models import Product

# Create your tests here.


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin@123')
        # self.client = APIClient()

        self.product_data = {
            'product_name': 'Test Product',
            'description': 'This is a test product',
            'manufacturer': 'Test Manufacturer',
            'serial_number': '123456789',
            'date_of_manufacture': '2022-03-20',
            'category': 'Test Category'
        }

        self.product = Product.objects.create(**self.product_data)

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.register_url = reverse('products-list')
        self.detail_url = reverse('products-detail', kwargs={'pk': self.product.pk})

    def test_product_get(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_product_create(self):
        url = reverse('products-list')
        response = self.client.post(url, self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_count = Product.objects.get(product_name=self.product_data['product_name']).count()
        self.assertEqual(product_count, 1)
    
    def test_product_update_authenticated(self):
        update_data = {
            'product_name': 'Test Product',
            'description': 'This is a test product',
            'manufacturer': 'Test Manufacturer',
            'serial_number': '123456789',
            'date_of_manufacture': '2022-03-20',
            'warranty_information': 'update Test warranty info',
            'category': 'Test Category'
        }
        
        response = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated_product.product_name, update_data['product_name'])
        self.assertEqual(updated_product.manufacturer, update_data['manufacturer'])
        self.assertEqual(updated_product.category, update_data['category'])

    def test_product_deletion_authenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        product_exists = Product.objects.filter(pk=self.product.pk).exists()
        self.assertFalse(product_exists)

    def test_product_get_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_update_unauthenticated(self):
        self.client.logout()
        response = self.client.patch(self.detail_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_deletion_unauthenticated(self):
        self.client.logout()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
