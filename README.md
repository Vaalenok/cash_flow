# Cash Flow

Веб-приложение для управления движением денежных средств (ДДС).
Тестовое задание.

## Установка и запуск

### 1. Клонирование репозитория

```
git clone https://github.com/Vaalenok/cash_flow.git
cd cash_flow
```

### 2. Создание виртуального окружения

```
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
.venv\Scripts\activate     # для Windows
```

### 3. Установка зависимостей

```
pip install -r requirements.txt
```

## Docker

Поднять контейнер командой ```docker-compose up``` 

После запуска приложение будет доступно по адресу:  
http://localhost:8000 (или http://127.0.0.1:8000/)

---

## Применение миграций

```
python manage.py migrate app
```

---

## Запуск проекта

```
python manage.py runserver
```

После запуска приложение будет доступно по адресу:  
http://localhost:8000 (или http://127.0.0.1:8000/)
