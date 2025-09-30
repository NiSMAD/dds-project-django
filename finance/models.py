from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=64, unique=True) # Бизнес/Личное/Налог

    # Определение метаданных модели
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        ordering = ["name"]

    def __str__(self):
        return self.name

class EntryType(models.Model):
    name = models.CharField(max_length=64, unique=True) # Пополнение/Списание

    class Meta:
        verbose_name = "Тип операции"
        verbose_name_plural = "Типы операций"
        ordering = ["name"]

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=64)
    entry_type = models.ForeignKey(EntryType, on_delete=models.PROTECT, related_name="categories")

    class Meta:
        unique_together = ("name", "entry_type")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["entry_type__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.entry_type})"

class Subcategory(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey
    
    class Meta:
        unique_together = ("name", "category")
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["category__name", "name"]

class Entry(models.Model):
    # "Дата создания записи — заполняется автоматически, но может быть изменена вручную"
    date = models.DateField(default=timezone.now)  # редактируемое
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="entries")
    entry_type = models.ForeignKey(EntryType, on_delete=models.PROTECT, related_name="entries")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="entries")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="entries")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)  # служебное
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ДДС запись"
        verbose_name_plural = "ДДС записи"
        ordering = ["-date", "-id"]

    def clean(self):
        # Бизнес-правила из ТЗ:
        # - нельзя выбрать подкатегорию, если она не связана с выбранной категорией
        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            raise ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

        # - нельзя выбрать категорию, если она не относится к выбранному типу
        if self.category and self.entry_type and self.category.entry_type_id != self.entry_type_id:
            raise ValidationError({"category": "Категория не принадлежит выбранному типу."})

    def save(self, *args, **kwargs):
        # Гарантируем серверную валидацию всегда
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} • {self.entry_type}/{self.category}/{self.subcategory} • {self.amount}"

