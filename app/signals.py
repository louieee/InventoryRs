from django.db.models.signals import pre_save
from django.dispatch import receiver

from app.models import Item, Supplier


@receiver(pre_save, sender=Item)
def clean_inventory_item(sender, instance, *args, **kwargs):
	instance.name = instance.name.title()


@receiver(pre_save, sender=Supplier)
def clean_supplier(sender, instance, *args, **kwargs):
	instance.name = instance.name.title()
