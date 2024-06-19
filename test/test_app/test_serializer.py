from rest_framework.test import APITestCase
from app.models import Item, Supplier
from api.v1.app.serializer import ItemSerializer, SupplierSerializer, SupplierListSerializer, ItemListSerializer, \
	MutateSupplierSerializer


class SupplierSerializerTest(APITestCase):

	def setUp(self):
		self.supplier = Supplier.objects.create(
			name="Test Supplier",
			email="test@supplier.com",
			telephone="1234567890",
			address="123 Test Address",
			state="Test State",
			country="Test Country"
		)
		self.item = Item.objects.create(
			name="Test Item",
			description="This is a test item.",
			price=10.99
		)
		self.supplier.items.add(self.item)

	def test_supplier_serializer(self):
		serializer = SupplierSerializer(self.supplier)
		data = serializer.data
		self.assertEqual(data['name'], self.supplier.name)
		self.assertEqual(data['email'], self.supplier.email)
		self.assertEqual(data['telephone'], self.supplier.telephone)
		self.assertEqual(data['address'], self.supplier.address)
		self.assertEqual(data['state'], self.supplier.state)
		self.assertEqual(data['country'], self.supplier.country)

	def test_supplier_list_serializer(self):
		suppliers = Supplier.objects.all()
		serializer = SupplierListSerializer(suppliers, many=True)
		data = serializer.data
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]['name'], self.supplier.name)

	def test_mutate_supplier_serializer_create(self):
		data = {
			"name": "New Supplier",
			"email": "new@supplier.com",
			"telephone": "+0987654321",
			"address": "456 New Address",
			"state": "New State",
			"country": "New Country",
			"items": [self.item.id]
		}
		serializer = MutateSupplierSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		supplier = serializer.save()
		self.assertEqual(supplier.name, "New Supplier")
		self.assertEqual(supplier.items.count(), 1)
		self.assertEqual(supplier.items.first().id, self.item.id)

	def test_mutate_supplier_serializer_update(self):
		data = {
			"name": "Updated Supplier",
			"email": "updated@supplier.com",
			"telephone": "+1234567890",
			"address": "123 Updated Address",
			"state": "Updated State",
			"country": "Updated Country",
			"items": [self.item.id]
		}
		serializer = MutateSupplierSerializer(self.supplier, data=data)
		self.assertTrue(serializer.is_valid())
		supplier = serializer.save()
		self.assertEqual(supplier.name, "Updated Supplier")
		self.assertEqual(supplier.items.count(), 1)
		self.assertEqual(supplier.items.first().id, self.item.id)


class ItemSerializerTest(APITestCase):

	def setUp(self):
		self.supplier = Supplier.objects.create(
			name="Test Supplier",
			email="test@supplier.com",
			telephone="1234567890",
			address="123 Test Address",
			state="Test State",
			country="Test Country"
		)
		self.item = Item.objects.create(
			name="Test Item",
			description="This is a test item.",
			price=10.99
		)
		self.supplier.items.add(self.item)

	def test_item_serializer(self):
		serializer = ItemSerializer(self.item)
		data = serializer.data
		self.assertEqual(data['name'], self.item.name)
		self.assertEqual(data['description'], self.item.description)
		self.assertEqual(data['price'], self.item.price)

	def test_item_list_serializer(self):
		items = Item.objects.all()
		serializer = ItemListSerializer(items, many=True)
		data = serializer.data
		self.assertEqual(len(data), 1)
		self.assertEqual(data[0]['name'], self.item.name)

	def test_item_create(self):
		data = {
			"name": "New Item",
			"description": "This is a new item.",
			"price": 20.99
		}
		serializer = ItemSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		item = serializer.save()
		self.assertEqual(item.name, "New Item")
		self.assertEqual(item.description, "This is a new item.")
		self.assertEqual(item.price, 20.99)

	def test_item_update(self):
		data = {
			"name": "Updated Item",
			"description": "This is an updated item.",
			"price": 30.99
		}
		serializer = ItemSerializer(self.item, data=data)
		self.assertTrue(serializer.is_valid())
		item = serializer.save()
		self.assertEqual(item.name, "Updated Item")
		self.assertEqual(item.description, "This is an updated item.")
		self.assertEqual(item.price, 30.99)