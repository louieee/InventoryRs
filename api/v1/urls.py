from django.urls import include, path

urlpatterns = [
	path("inventory/", include("api.v1.app.urls")),
	path("auth/", include("api.v1.auth.urls"))
]