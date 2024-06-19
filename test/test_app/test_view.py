from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.models import Item, Supplier


class ItemModelViewSetTests(APITestCase):

    def setUp(self):
        self.item = Item.objects.create(name='Item1', description='Description1', price=10.0)
        self.supplier = Supplier.objects.create(name='Supplier1', email='supplier1@example.com', telephone='123456789',
                                                address='Address1', state='State1', country='Country1')
        self.supplier.items.add(self.item)
        self.item_url = f"/api/v1/inventory/items/{self.item.id}/"
        self.supplier_url = f"/api/v1/inventory/suppliers/{self.supplier.id}/"
        self.items_url = "/api/v1/inventory/items/"
        self.suppliers_url = "/api/v1/inventory/suppliers/"
        self.employee = User.objects.create(username="employee", password="employee")
        self.client.force_authenticate(self.employee)

    def test_create_item(self):
        data = {
            'name': 'Item2',
            'description': 'Description2',
            'price': 20.0
        }
        response = self.client.post(self.items_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_item(self):
        data = {
            'name': 'Item1 Updated',
            'description': 'Description1 Updated',
            'price': 15.0
        }
        response = self.client.put(self.item_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Item1 Updated')

    def test_delete_item(self):
        response = self.client.delete(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

    def test_restore_item(self):
        self.client.delete(self.item_url)
        restore_url = self.item_url = f"/api/v1/inventory/items/{self.item.id}/restore/"
        response = self.client.post(restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(Item.objects.get(id=self.item.id).deleted_at)

    def test_retrieve_item(self):
        response = self.client.get(self.item_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_list_items(self):
        response = self.client.get(self.items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_item_suppliers(self):
        suppliers_url = self.item_url = f"/api/v1/inventory/items/{self.item.id}/suppliers/"
        response = self.client.get(suppliers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]['name'], self.supplier.name)


class SupplierModelViewSetTests(APITestCase):

    def setUp(self):
        self.employee = User.objects.create(username="employee", password="employee")
        self.item = Item.objects.create(name='Item1', description='Description1', price=10.0)
        self.supplier = Supplier.objects.create(name='Supplier1', email='supplier1@example.com', telephone='123456789',
                                                address='Address1', state='State1', country='Country1')
        self.supplier.items.add(self.item)
        self.item_url = f"/api/v1/inventory/items/{self.item.id}/"
        self.supplier_url = f"/api/v1/inventory/suppliers/{self.supplier.id}/"
        self.items_url = "/api/v1/inventory/items/"
        self.suppliers_url = "/api/v1/inventory/suppliers/"
        self.client.force_authenticate(self.employee)

    def test_create_supplier(self):
        data = {
            'name': 'Supplier2',
            'email': 'supplier2@example.com',
            'telephone': '+987654321',
            'address': 'Address2',
            'state': 'State2',
            'country': 'Country2',
            'items': [self.item.id]
        }
        response = self.client.post(self.suppliers_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_supplier(self):
        data = {
            'name': 'Supplier1 Updated',
            'email': 'supplier1_updated@example.com',
            'telephone': '+1234567890',
            'address': 'Address1 Updated',
            'state': 'State1',
            'country': 'Country1',
            'items': [self.item.id]
        }
        response = self.client.put(self.supplier_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Supplier1 Updated')

    def test_delete_supplier(self):
        response = self.client.delete(self.supplier_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())

    def test_restore_supplier(self):
        self.client.delete(self.supplier_url)
        restore_url = self.item_url = f"/api/v1/inventory/suppliers/{self.supplier.id}/restore/"
        response = self.client.post(restore_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(Supplier.objects.get(id=self.supplier.id).deleted_at)

    def test_retrieve_supplier(self):
        response = self.client.get(self.supplier_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.supplier.name)

    def test_list_suppliers(self):
        response = self.client.get(self.suppliers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_supplier_items(self):
        items_url = self.item_url = f"/api/v1/inventory/suppliers/{self.supplier.id}/items/"
        response = self.client.get(items_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]['name'], self.item.name)
