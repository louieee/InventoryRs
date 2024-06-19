from rest_framework.routers import SimpleRouter
from .views import ItemModelViewSet, SupplierModelViewSet
router = SimpleRouter()
router.register("items", ItemModelViewSet, basename="items")
router.register("suppliers", SupplierModelViewSet, basename="suppliers")
urlpatterns = []

urlpatterns.extend(router.urls)
