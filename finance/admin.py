from django.contrib import admin
from .models import Status, EntryType, Category, Subcategory, Entry

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(EntryType)
class EntryTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "entry_type"]
    list_filter = ["entry_type"]
    search_fields = ["name"]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "category_entry_type"]
    list_filter = ["category__entry_type", "category"]
    search_fields = ["name"]

    @admin.display(ordering="category__entry_type__name", description="Тип")
    def category_entry_type(self, obj):
        return obj.category.entry_type.name

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ["date", "status", "entry_type", "category", "subcategory", "amount"]
    list_filter = ["status", "entry_type", "category", "subcategory", ("date", admin.DateFieldListFilter)]
    search_fields = ["comment"]
