# 💰 DDS Project — Django/DRF веб-сервис для управления движением денежных средств

[![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.15-red?logo=fastapi\&logoColor=white)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Веб-приложение для учёта и анализа ДДС (движения денежных средств).
Поддерживает работу через веб-интерфейс и REST API.

---

## ✨ Возможности

* 📑 CRUD-операции над записями ДДС (создание, просмотр, редактирование, удаление).
* 🔎 Фильтрация по:

  * периоду дат
  * статусу (Бизнес, Личное, Налог, ...)
  * типу операции (Пополнение, Списание)
  * категории (Маркетинг, Инфраструктура и др.)
  * подкатегории (Avito, VPS и т.п.)
* ⚙️ Управление справочниками (статусы, типы, категории, подкатегории).
* ✅ Валидация:

  * на клиенте (HTML5 формы)
  * на сервере (Django `clean()`)
* 🔗 REST API на Django REST Framework с фильтрацией и сериализаторами.
* 🖥️ Мини-фронтенд (SPA) на чистом JS, использующий API (`/spa/`).

---


## 🚀 Установка и запуск

### 1. Клонировать проект

```bash
git clone https://github.com/<your-username>/dds_project.git
cd dds_project
```

### 2. Создать виртуальное окружение

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Применить миграции

```bash
python manage.py migrate
```

### 5. Создать суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Запустить сервер

```bash
python manage.py runserver
```

---

## 🌐 Доступные страницы

* **Главная страница (таблица записей)** → [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* **CRUD записей (создание, редактирование, удаление)**
* **Справочники** → [http://127.0.0.1:8000/dictionaries/](http://127.0.0.1:8000/dictionaries/)
* **Админка** → [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
* **Фронтенд (SPA на JS)** → [http://127.0.0.1:8000/spa/](http://127.0.0.1:8000/spa/)
* **REST API (DRF)** → [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

---

## 🔌 REST API

Примеры:

### Получить все записи

```http
GET /api/entries/
```

### Фильтрация

```http
GET /api/entries/?date=2025-01-01&entry_type=1&status=2
```

### Создать запись

```http
POST /api/entries/
Content-Type: application/json

{
  "date": "2025-01-01",
  "amount": "1500.00",
  "comment": "Пополнение",
  "status_id": 1,
  "entry_type_id": 1,
  "category_id": 3,
  "subcategory_id": 7
}
```

Ответ:

```json
{
  "id": 12,
  "date": "2025-01-01",
  "amount": "1500.00",
  "comment": "Пополнение",
  "status": {"id":1,"name":"Бизнес"},
  "entry_type": {"id":1,"name":"Пополнение"},
  "category": {"id":3,"name":"Маркетинг", ...},
  "subcategory": {"id":7,"name":"Avito", ...}
}
```

---

## 🧪 Тестирование

```bash
pytest -q
```

Тесты проверяют бизнес-правила:

* подкатегория принадлежит выбранной категории
* категория соответствует выбранному типу

---

## 🛠️ Стек технологий

* **Backend:** Django 5, Django REST Framework
* **DB:** SQLite
* **Frontend:** Django Templates, Bootstrap 5, Vanilla JS
* **Тесты:** pytest
