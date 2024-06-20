from django.db import models

from core.models import BaseModel
from core.validators import phone_number_validator


# Create your models here.

class Item(BaseModel):
	"""
	Each item should have a name, a detailed description, a price, and the date when it was added to the
	inventory.
	"""
	name = models.CharField(max_length=200, unique=True)
	description = models.TextField()
	price = models.FloatField(default=0)

	def suppliers(self):
		return Supplier.objects.filter(items__id=self.id)

	def __str__(self):
		return self.name

class Supplier(BaseModel):
	"""
	Each supplier should have a name, contact information, and a list of items they supply.
	"""
	name = models.CharField(max_length=200, unique=True)
	email = models.EmailField(unique=True)
	telephone = models.CharField(max_length=20, unique=True, validators=[phone_number_validator])
	address = models.TextField()
	state = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	items = models.ManyToManyField("app.Item")

	def __str__(self):
		return self.name
