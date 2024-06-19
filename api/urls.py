from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

swagger_view = get_schema_view(
	info=openapi.Info(
		title=f"Inventory Backend API",
		default_version="Version 1",
		terms_of_service="https://inventory.com",
		license=openapi.License(name="BSD License"),
	),
	public=True,
	permission_classes=[permissions.AllowAny],
)

urlpatterns = [
	path("v1/", include("api.v1.urls")),
	path("docs/", swagger_view.with_ui("swagger", cache_timeout=0), name="swagger_docs_v1")
]
