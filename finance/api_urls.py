from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import StatusViewSet, EntryTypeViewSet, CategoryViewSet, SubcategoryViewSet, EntryViewSet

router = DefaultRouter()
router.register(r"statuses", StatusViewSet)
router.register(r"types", EntryTypeViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"subcategories", SubcategoryViewSet)
router.register(r"entries", EntryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
