import uuid

from django.db import models
from django.db.models import Manager
from django.utils import timezone


# Create your models here.


class BaseManager(Manager):
	def __init__(self, *args, **kwargs):
		self.active_only = kwargs.pop("active_only", True)
		super().__init__(*args, **kwargs)

	def get_queryset(self):
		if self.active_only is True:
			return super().get_queryset().filter(deleted_at__isnull=True)
		return super().get_queryset()


class BaseModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(blank=True, null=True, editable=False)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	objects = BaseManager()
	all_objects = BaseManager(active_only=False)

	class Meta:
		abstract = True

	def delete(self, *args, **kwargs):
		""" function to allow soft delete """
		self.deleted_at = timezone.now()
		self.save()

	def restore(self):
		self.deleted_at = None
		self.save()

	def hard_delete(self):
		super(BaseModel, self).delete()
