from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Entry, Status, EntryType, Category, Subcategory
from .forms import EntryForm
from django.views.generic import TemplateView

class EntrySPAView(TemplateView):
    template_name = "finance/spa.html"

class EntryListView(ListView):
    model = Entry
    template_name = "finance/entry_list.html"
    context_object_name = "entries"
    paginate_by = 20
    
    def get_queryset(self):
        qs = super().get_queryset().select_related("status", "entry_type", "category", "subcategory")
        # Фильтрация по ТЗ: период дат, статус, тип, категория, подкатегория
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        status_id = self.request.GET.get("status")
        entry_type_id = self.request.GET.get("entry_type")
        category_id = self.request.GET.get("category")
        subcategory_id = self.request.GET.get("subcategory")

        if date_from:
            qs = qs.filter(date__gte=date_from)
        if date_to:
            qs = qs.filter(date__lte=date_to)
        if status_id:
            qs = qs.filter(status_id=status_id)
        if entry_type_id:
            qs = qs.filter(entry_type_id=entry_type_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.all()
        ctx["entry_types"] = EntryType.objects.all()
        # Для каскада фильтров фронтэндом подгружаем списки целиком (просто)
        ctx["categories"] = Category.objects.select_related("entry_type").all()
        ctx["subcategories"] = Subcategory.objects.select_related("category", "category__entry_type").all()
        return ctx


class EntryCreateView(CreateView):
    model = Entry
    form_class = EntryForm
    template_name = "finance/entry_form.html"
    success_url = reverse_lazy("finance:entry_list")


class EntryUpdateView(UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = "finance/entry_form.html"
    success_url = reverse_lazy("finance:entry_list")


class EntryDeleteView(DeleteView):
    model = Entry
    template_name = "finance/entry_confirm_delete.html"
    success_url = reverse_lazy("finance:entry_list")


class DictionariesView(TemplateView):
    """
    Простейшая страница управления справочниками:
    - В реальном проекте можно сделать полноценный CRUD,
      здесь используем admin для полного CRUD, а на этой странице — быстрые формы добавления.
      CRUD - Create/Read/Update/Delete
    """
    template_name = "finance/dictionaries.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.all()
        ctx["types"] = EntryType.objects.all()
        ctx["categories"] = Category.objects.select_related("entry_type").all()
        ctx["subcategories"] = Subcategory.objects.select_related("category", "category__entry_type").all()
        return ctx
