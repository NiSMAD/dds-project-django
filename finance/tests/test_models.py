import pytest
from django.core.exceptions import ValidationError
from finance.models import Status, EntryType, Category, Subcategory, Entry
from django.utils import timezone

@pytest.mark.django_db
def test_entry_validation_relations():
    status = Status.objects.create(name="Бизнес")
    t_topup = EntryType.objects.create(name="Пополнение")
    t_spend = EntryType.objects.create(name="Списание")

    cat_mkt = Category.objects.create(name="Маркетинг", entry_type=t_spend)
    cat_infra = Category.objects.create(name="Инфраструктура", entry_type=t_spend)
    sub_avito = Subcategory.objects.create(name="Avito", category=cat_mkt)
    sub_vps = Subcategory.objects.create(name="VPS", category=cat_infra)

    # OK: тип=Списание, категория=Маркетинг (того же типа), подкатегория=Avito (той же категории)
    e1 = Entry(
        date=timezone.now().date(),
        status=status,
        entry_type=t_spend,
        category=cat_mkt,
        subcategory=sub_avito,
        amount=1000
    )
    e1.full_clean()  # не должно бросать

    # Ошибка: подкатегория "VPS" не принадлежит категории "Маркетинг"
    e2 = Entry(
        date=timezone.now().date(),
        status=status,
        entry_type=t_spend,
        category=cat_mkt,
        subcategory=sub_vps,
        amount=500
    )
    with pytest.raises(ValidationError):
        e2.full_clean()

    # Ошибка: категория "Маркетинг" не принадлежит типу "Пополнение"
    e3 = Entry(
        date=timezone.now().date(),
        status=status,
        entry_type=t_topup,
        category=cat_mkt,
        subcategory=sub_avito,
        amount=500
    )
    with pytest.raises(ValidationError):
        e3.full_clean()
