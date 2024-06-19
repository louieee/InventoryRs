from django.test import TestCase
from django.utils import timezone
from app.models import Item, Supplier
from django.core.exceptions import ObjectDoesNotExist


class ModelTest(TestCase):

	def setUp(self):
		# Set up a supplier instance to associate with InventoryItem
		self.supplier = Supplier.objects.create(
			name="Test supplier",
			email="test_supplier@example.com",
			telephone="+23480808080",
			address="1000 Box street.",
			state="Lagos",
			country="Nigeria"
		)
		# Create an InventoryItem instance
		self.item = Item.objects.create(
			name="Test item",
			description="This is a test item.",
			price=10.99
		)
		self.supplier.items.add(self.item)

	def test_item_creation(self):
		# Test the item was created correctly
		self.assertEqual(self.item.name, "Test Item", "name is in title case")
		self.assertEqual(self.item.description, "This is a test item.")
		self.assertEqual(self.item.price, 10.99)
		self.assertIsNotNone(self.item.created_at)
		self.assertIsNotNone(self.item.updated_at)

	def test_supplier_creation(self):
		# Test the supplier was created correctly
		self.assertEqual(self.supplier.name, "Test Supplier", "name is in title case")
		self.assertEqual(self.supplier.state, "Lagos")
		self.assertEqual(self.supplier.country, "Nigeria")
		self.assertEqual(self.supplier.address, "1000 Box street.")
		self.assertEqual(self.supplier.email, "test_supplier@example.com")
		self.assertEqual(self.supplier.telephone, "+23480808080")
		self.assertIn(self.item, self.supplier.items.all())
		self.assertIsNotNone(self.item.created_at)
		self.assertIsNotNone(self.item.updated_at)

	def test_item_soft_delete(self):
		# Test the soft delete functionality
		self.item.delete()
		self.assertIsNotNone(self.item.deleted_at)

		# Verify the item is not accessible through the default manager
		with self.assertRaises(ObjectDoesNotExist):
			Item.objects.get(id=self.item.id)

		# Verify the item is accessible through the all_objects manager
		item = Item.all_objects.get(id=self.item.id)
		self.assertEqual(item, self.item)

	def test_item_restore(self):
		# Test the restore functionality
		self.item.delete()
		self.item.restore()
		self.assertIsNone(self.item.deleted_at)

		# Verify the item is accessible through the default manager
		item = Item.objects.get(id=self.item.id)
		self.assertEqual(item, self.item)

	def test_item_hard_delete(self):
		# Test the hard delete functionality
		item_id = self.item.id
		self.item.hard_delete()
		with self.assertRaises(ObjectDoesNotExist):
			Item.all_objects.get(id=item_id)

	def test_item_str(self):
		# Test the __str__ method, if you have one
		self.assertEqual(str(self.item), "Test Item")

	def test_item_suppliers_method(self):
		# Test the inventory item supplier method works as expected
		suppliers = self.item.suppliers()
		self.assertEqual(suppliers.count(), 1)
		self.assertIn(self.supplier, suppliers)
