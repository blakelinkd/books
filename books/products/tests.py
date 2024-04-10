from datetime import timezone
from decimal import Decimal
from django.test import RequestFactory, TestCase
from django.urls import reverse

from rest_framework.test import APIRequestFactory, APITestCase

from products.models import Product
from products.views import ProductList, ProductDetail

class ProductListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product1 = Product.objects.create(name='Product 1', price=10.00, inventory=10)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, inventory=20)

    def test_get(self):
        request = self.factory.get(reverse('products:product-list'))
        response = ProductList.as_view()(request)

        self.assertEqual(response.status_code, 200)

        # Extract only the relevant fields from the response data
        actual_data = [
            {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'inventory': product['inventory'],
            }
            for product in response.data
        ]

        expected_data = [
            {
                'id': self.product1.id,
                'name': 'Product 1',
                'price': '10.00',
                'inventory': 10,
            },
            {
                'id': self.product2.id,
                'name': 'Product 2',
                'price': '20.00',
                'inventory': 20,
            },
        ]

        self.assertListEqual(actual_data, expected_data)

    def test_post(self):
        data = {'name': 'Product 3', 'description': 'Test product', 'price': Decimal('30.00'), 'inventory': 30}
        request = self.factory.post(reverse('products:product-list'), data, format='json')
        response = ProductList.as_view()(request)

        # Check the response status code
        self.assertEqual(response.status_code, 201)

        # Check the response data
        expected_data = {
            'id': response.data['id'],
            'name': 'Product 3',
            'description': 'Test product',
            'price': '30.00',
            'inventory': 30,
            'created_at': response.data['created_at'],
            'updated_at': response.data['updated_at'],
        }
        self.assertDictEqual(response.data, expected_data)

        # Check the created object in the database
        self.assertEqual(Product.objects.count(), 3)
        product = Product.objects.get(id=response.data['id'])
        self.assertEqual(product.name, 'Product 3')
        self.assertEqual(product.description, 'Test product')
        self.assertEqual(float(product.price), 30.00)
        self.assertEqual(product.inventory, 30)
        
class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(name='Product 1', price=10.00, inventory=10)

    def test_get(self):
        request = self.factory.get(reverse('products:product-detail', args=[self.product.id]))
        response = ProductDetail.as_view()(request, pk=self.product.id)

        self.assertEqual(response.status_code, 200)

        # Extract only the relevant fields from the response data
        response_data = {
            'id': response.data['id'],
            'name': response.data['name'],
            'description': response.data['description'],
            'price': response.data['price'],
            'inventory': response.data['inventory'],
        }

        self.assertEqual(response_data, {
            'id': self.product.id,
            'name': 'Product 1',
            'description': '',
            'price': '10.00',
            'inventory': 10,
        })

    def test_put(self):
        data = {'name': 'Product 1 (updated)', 'price': '20.00', 'inventory': 20}
        request = self.factory.put(
        reverse('products:product-detail', args=[self.product.id]),
        data=data,
        content_type='application/json',
        )
        response = ProductDetail.as_view()(request, pk=self.product.id)
        self.assertEqual(response.status_code, 200)

        # Extract only the relevant fields from the response data
        response_data = {
            'id': response.data['id'],
            'name': response.data['name'],
            'description': response.data['description'],
            'price': response.data['price'],
            'inventory': response.data['inventory'],
        }

        self.assertEqual(response_data, {
            'id': self.product.id,
            'name': 'Product 1 (updated)',
            'description': self.product.description,
            'price': '20.00',
            'inventory': 20,
        })

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Product 1 (updated)')
        self.assertEqual(self.product.price, 20.00)
        self.assertEqual(self.product.inventory, 20)

    def test_delete(self):
        request = self.factory.delete(reverse('products:product-detail', args=[self.product.id]))
        response = ProductDetail.as_view()(request, pk=self.product.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 0)

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.product1 = Product.objects.create(name='Product 1', price=10.00, inventory=10)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, inventory=20)

from django.utils import timezone

class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.product1 = Product.objects.create(name='Product 1', price=10.00, inventory=10)
        self.product2 = Product.objects.create(name='Product 2', price=20.00, inventory=20)

    def test_list(self):
        request = self.factory.get(reverse('products:product-list'))
        response = ProductList.as_view()(request)
        self.assertEqual(response.status_code, 200)

        expected_data = [
            {'id': self.product1.id, 'name': 'Product 1', 'description': '', 'price': '10.00', 'inventory': 10},
            {'id': self.product2.id, 'name': 'Product 2', 'description': '', 'price': '20.00', 'inventory': 20},
        ]

        actual_data = [{
            'id': product['id'],
            'name': product['name'],
            'description': product['description'],
            'price': product['price'],
            'inventory': product['inventory'],
        } for product in sorted(response.data, key=lambda x: x['id'])]

        self.assertListEqual(expected_data, actual_data)

    def test_create(self):
        data = {'name': 'Product 3', 'price': '30.00', 'inventory': 30, 'description': 'Test product'}
        request = self.factory.post(reverse('products:product-list'), data, format='json')
        response = ProductList.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.maxDiff = None  # Print the full difference between the expected and actual values in case of failure
        expected_data = {'id': 3, 'name': 'Product 3', 'price': '30.00', 'inventory': 30, 'description': 'Test product', 'created_at': response.data['created_at'], 'updated_at': response.data['updated_at']}
        self.assertEqual(response.data, expected_data)
        self.assertEqual(Product.objects.count(), 3)


    def test_retrieve(self):
        request = self.factory.get(reverse('products:product-detail', args=[self.product1.id]))
        response = ProductDetail.as_view()(request, pk=self.product1.id)
        self.assertEqual(response.status_code, 200)

        # Remove the 'created_at' and 'updated_at' fields from the response data
        response_data = {
            'id': response.data['id'],
            'name': response.data['name'],
            'description': response.data['description'],
            'price': response.data['price'],
            'inventory': response.data['inventory'],
        }

        self.assertEqual(response_data, {
            'id': self.product1.id,
            'name': 'Product 1',
            'description': self.product1.description,
            'price': '10.00',
            'inventory': 10,
        })

    def test_update(self):
        data = {'name': 'Product 1 (updated)', 'price': '20.00', 'inventory': 20}
        request = self.factory.put(reverse('products:product-detail', args=[self.product1.id]), data, format='json')
        response = ProductDetail.as_view()(request, pk=self.product1.id)

        self.assertEqual(response.status_code, 200)

        # Extract only the relevant fields from the response data
        response_data = {
            'id': response.data['id'],
            'name': response.data['name'],
            'price': response.data['price'],
            'inventory': response.data['inventory'],
        }

        self.assertEqual(response_data, {
            'id': self.product1.id,
            'name': 'Product 1 (updated)',
            'price': '20.00',
            'inventory': 20,
        })

        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Product 1 (updated)')
        self.assertEqual(self.product1.price, 20.00)
        self.assertEqual(self.product1.inventory, 20)

    def test_delete(self):
        request = self.factory.delete(reverse('products:product-detail', args=[self.product1.id]))
        response = ProductDetail.as_view()(request, pk=self.product1.id)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Product.objects.count(), 1)
