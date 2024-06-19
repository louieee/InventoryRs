from django.db import transaction
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.app.serializer import ItemSerializer, ItemListSerializer, SupplierListSerializer, SupplierSerializer, \
	MutateSupplierSerializer
from app.models import Item, Supplier
from core.serializers import BaseModelViewSet
from core.views import visibility_query, page_query, page_size_query, hard_delete_query


class ItemModelViewSet(BaseModelViewSet):
	serializer_class = ItemSerializer
	queryset = Item.all_objects.order_by("name")  # return all items both deleted and active
	http_method_names = ["get", "post", "delete", "put"]
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		operation_summary="creates an item",
	)
	@transaction.atomic
	def create(self, request, *args, **kwargs):
		return super().create(request, *args, **kwargs)

	@swagger_auto_schema(
		operation_summary="updates an item"
	)
	@transaction.atomic
	def update(self, request, *args, **kwargs):
		return super().update(request, *args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[hard_delete_query],
		operation_summary="deletes an item (soft & hard delete)"
	)
	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		hard_delete = self.request.query_params.get("hard_delete", "false")
		hard_delete = hard_delete == "true"
		return super().destroy(request, hard_delete=hard_delete, *args, **kwargs)

	@swagger_auto_schema(
		request_body=no_body,
		operation_summary="restores a deleted item",
	)
	@action(detail=True, methods=["POST"])
	def restore(self, request, *args, **kwargs):
		with transaction.atomic():
			self.default_Visibility = self.VisibilityChoices.DELETED
			instance: Item = self.get_object()
			instance.restore()
			return Response(self.serializer_class(instance).data)

	@swagger_auto_schema(
		operation_summary="retrieves details of an item",
	)
	def retrieve(self, request, *args, **kwargs):
		return super().retrieve(request, args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[visibility_query],
		operation_summary="retrieves list of items",
	)
	def list(self, request, *args, **kwargs):
		self.default_Visibility = self.VisibilityChoices.ACTIVE
		self.serializer_class = ItemListSerializer
		return super().list(request, args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[page_query, page_size_query],
		operation_summary="retrieves list of an item's suppliers",
	)
	@action(detail=True, methods=["GET"])
	def suppliers(self, request, *args, **kwargs):
		self.serializer_class = SupplierListSerializer
		item = self.get_object()
		return self.get_list(queryset=item.suppliers().order_by("name"))


class SupplierModelViewSet(BaseModelViewSet):
	serializer_class = SupplierSerializer
	queryset = Supplier.all_objects.order_by("name")  # return all suppliers both deleted and active
	http_method_names = ["get", "post", "delete", "put"]
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		request_body=MutateSupplierSerializer,
		operation_summary="creates a new supplier",
	)
	@transaction.atomic
	def create(self, request, *args, **kwargs):
		self.serializer_class = MutateSupplierSerializer
		return super().create(request, *args, **kwargs)

	@swagger_auto_schema(
		request_body=MutateSupplierSerializer,
		operation_summary="updates a supplier",
	)
	@transaction.atomic
	def update(self, request, *args, **kwargs):
		self.serializer_class = MutateSupplierSerializer
		return super().update(request, *args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[hard_delete_query],
		operation_summary="deletes a supplier",
	)
	@transaction.atomic
	def destroy(self, request, *args, **kwargs):
		hard_delete = self.request.query_params.get("hard_delete", "false")
		hard_delete = hard_delete == "true"
		return super().destroy(request, hard_delete=hard_delete, *args, **kwargs)

	@swagger_auto_schema(
		request_body=no_body,
		operation_summary="restores a deleted supplier"
	)
	@action(detail=True, methods=["POST"])
	def restore(self, request, *args, **kwargs):
		with transaction.atomic():
			self.default_Visibility = self.VisibilityChoices.DELETED
			instance = self.get_object()
			instance.restore()
			return Response(self.serializer_class(instance).data)

	@swagger_auto_schema(
		operation_summary="retrieves a supplier",
	)
	def retrieve(self, request, *args, **kwargs):
		return super().retrieve(request, args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[visibility_query],
		operation_summary="retrieves a list of suppliers",
	)
	def list(self, request, *args, **kwargs):
		self.default_Visibility = self.VisibilityChoices.ACTIVE
		self.serializer_class = SupplierListSerializer
		return super().list(request, args, **kwargs)

	@swagger_auto_schema(
		manual_parameters=[page_query, page_size_query],
		operation_summary="retrieves a supplier's items",
	)
	@action(detail=True, methods=["GET"])
	def items(self, request, *args, **kwargs):
		self.serializer_class = SupplierListSerializer
		supplier: Supplier = self.get_object()
		return self.get_list(queryset=supplier.items.order_by("name"))
