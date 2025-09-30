from django.urls import path
from . import views

app_name = "finance"

from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    # список записей (главная страница)
    path("", views.EntryListView.as_view(), name="entry_list"),

    # CRUD для записей ДДС
    path("entries/new/", views.EntryCreateView.as_view(), name="entry_create"),
    path("entries/<int:pk>/edit/", views.EntryUpdateView.as_view(), name="entry_update"),
    path("entries/<int:pk>/delete/", views.EntryDeleteView.as_view(), name="entry_delete"),

    # управление справочниками
    path("dictionaries/", views.DictionariesView.as_view(), name="dictionaries"),

    # фронтенд на REST API (SPA)
    path("spa/", views.EntrySPAView.as_view(), name="spa"),
]
