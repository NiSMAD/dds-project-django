from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Status, EntryType, Category, Subcategory, Entry
from .serializers import (
    StatusSerializer, EntryTypeSerializer, CategorySerializer, SubcategorySerializer, EntrySerializer
)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by("name")
    serializer_class = StatusSerializer

class EntryTypeViewSet(viewsets.ModelViewSet):
    queryset = EntryType.objects.all().order_by("name")
    serializer_class = EntryTypeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.select_related("entry_type").all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["entry_type"]

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.select_related("category", "category__entry_type").all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category", "category__entry_type"]

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.select_related("status", "entry_type", "category", "subcategory").all()
    serializer_class = EntrySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["status", "entry_type", "category", "subcategory", "date"]
    ordering_fields = ["date", "id"]