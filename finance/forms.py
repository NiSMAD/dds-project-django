from django import forms
from .models import Entry, Category, Subcategory

class EntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Entry
        fields = ["date", "status", "entry_type", "category", "subcategory", "amount", "comment"]
        widgets = {
            "amount": forms.NumberInput(attrs={"step": "0.01", "min": "0", "required": True}),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Фильтруем категории по выбранному типу (при редактировании)
        if "entry_type" in self.data:
            try:
                entry_type_id = int(self.data.get("entry_type"))
                self.fields["category"].queryset = Category.objects.filter(entry_type_id=entry_type_id)
            except (TypeError, ValueError):
                self.fields["category"].queryset = Category.objects.none()
        elif self.instance.pk:
            self.fields["category"].queryset = Category.objects.filter(entry_type=self.instance.entry_type)
        else:
            self.fields["category"].queryset = Category.objects.none()

        # Фильтруем подкатегории по выбранной категории
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=category_id)
            except (TypeError, ValueError):
                self.fields["subcategory"].queryset = Subcategory.objects.none()
        elif self.instance.pk:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(category=self.instance.category)
        else:
            self.fields["subcategory"].queryset = Subcategory.objects.none()
