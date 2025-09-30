from rest_framework import serializers
from .models import Status, EntryType, Category, Subcategory, Entry

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name"]

class EntryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryType
        fields = ["id", "name"]

class CategorySerializer(serializers.ModelSerializer):
    entry_type = EntryTypeSerializer(read_only=True)
    entry_type_id = serializers.PrimaryKeyRelatedField(
        queryset=EntryType.objects.all(), source="entry_type", write_only=True
    )

    class Meta:
        model = Category
        fields = ["id", "name", "entry_type", "entry_type_id"]

class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Subcategory
        fields = ["id", "name", "category", "category_id"]

class EntrySerializer(serializers.ModelSerializer):
    # read-only вложенные
    status = StatusSerializer(read_only=True)
    entry_type = EntryTypeSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)

    # write-only id-поля
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), source="status", write_only=True)
    entry_type_id = serializers.PrimaryKeyRelatedField(queryset=EntryType.objects.all(), source="entry_type", write_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all(), source="subcategory", write_only=True)

    class Meta:
        model = Entry
        fields = [
            "id", "date", "amount", "comment",
            "status", "entry_type", "category", "subcategory",
            "status_id", "entry_type_id", "category_id", "subcategory_id",
            "created_at", "updated_at"
        ]
