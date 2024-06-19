from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from app.models import Item, Supplier

"""
Employees need capabilities to add, view, update, and remove items from the inventory.
There should be functionalities to add new suppliers, update their details, and view their information.
"""


class SupplierListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Supplier
		fields = ("id", "name")


class ItemListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = ("id", "name")


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = "__all__"

	def validate(self, attrs):
		if not self.instance:
			if Item.all_objects.filter(name=attrs["name"]).exists():
				raise ValidationError("item with this name already exists.")
		return super().validate(attrs)


class SupplierSerializer(serializers.ModelSerializer):
	class Meta:
		model = Supplier
		exclude = ("items",)


class MutateSupplierSerializer(serializers.ModelSerializer):
	items = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), many=True, allow_empty=True)

	class Meta:
		model = Supplier
		fields = "__all__"

	def validate(self, attrs):
		if not self.instance:
			if Supplier.all_objects.filter(name=attrs["name"].title()).exists():
				raise ValidationError("supplier with this name already exists.")
			if Supplier.all_objects.filter(email=attrs["email"].lower()).exists():
				raise ValidationError("supplier with this email already exists.")
			if Supplier.all_objects.filter(telephone=attrs["telephone"].lower()).exists():
				raise ValidationError("supplier with this telephone already exists.")
		return super().validate(attrs)

	def update(self, instance: Supplier, validated_data):
		items = validated_data.pop("items", [])
		instance = super().update(instance, validated_data)
		instance.items.add(*items)
		return instance

	def create(self, validated_data):
		items = validated_data.pop("items", [])
		instance = super().create(validated_data)
		instance.items.add(*items)
		return instance
