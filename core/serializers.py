from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
	class Meta:
		abstract = True

	class VisibilityChoices:
		ALL = "all"
		DELETED = "deleted"
		ACTIVE = "active"

	default_Visibility = VisibilityChoices.ALL

	def get_queryset(self):
		"""
		adds visibility toggle ability to the modelviewset to toggle between deleted records,
		active records and all records
		"""
		visibility_status = self.request.query_params.get("visibility", self.default_Visibility)
		if visibility_status == self.VisibilityChoices.ACTIVE:
			return self.queryset.filter(deleted_at__isnull=True)
		elif visibility_status == self.VisibilityChoices.DELETED:
			return self.queryset.filter(deleted_at__isnull=False)
		return self.queryset

	def get_list(self, queryset):
		""" function to return paginated queryset in a custom action view"""
		page = self.paginate_queryset(queryset)
		if page is not None:
			serializer = self.get_serializer(page, many=True)
			return self.get_paginated_response(serializer.data)
		serializer = self.get_serializer(queryset, many=True)
		return Response(serializer.data)

	def destroy(self, request, *args, **kwargs):
		""" function to enable soft delete function in the modelviewset"""
		hard_delete = kwargs.get("hard_delete", False)
		instance = self.get_object()
		self.perform_destroy(instance=instance, hard_delete=hard_delete)
		return Response(status=status.HTTP_204_NO_CONTENT)

	def perform_destroy(self, instance, hard_delete=False):
		if hard_delete:
			instance.hard_delete()
		else:
			instance.delete()
