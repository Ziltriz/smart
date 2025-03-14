# smart
# Тестовое задание: Django + Stripe API

## Описание

Необходимо реализовать бэкенд на Django, интегрированный с платежной системой Stripe. Сервер должен предоставлять API для создания платежных форм и обработки платежей через Stripe. Решение должно быть загружено на GitHub и развернуто онлайн для тестирования.

---

## Задание

### Основные требования:
1. **Модель `Item`:**
   - Поля: `name`, `description`, `price`.
   - Модель должна быть доступна для управления через Django Admin.

2. **API методы:**
   - **GET `/buy/{id}`:**
     - Возвращает `session_id` для оплаты выбранного товара через Stripe.
     - Использует `stripe.checkout.Session.create(...)` для создания сессии.
   - **GET `/item/{id}`:**
     - Возвращает HTML-страницу с информацией о товаре и кнопкой "Buy".
     - По нажатию на кнопку происходит запрос на `/buy/{id}`, получение `session_id` и редирект на Stripe Checkout форму с помощью JS библиотеки Stripe.

3. **Деплой:**
   - Решение должно быть развернуто онлайн и доступно для тестирования.
   - Предоставьте ссылку на решение и доступ к админке.

---

## Бонусные задачи

1. **Docker:** Запуск приложения с использованием Docker.
2. **Environment Variables:** Использование переменных окружения для настройки.
3. **Django Admin:** Настройка просмотра моделей в Django Admin.
4. **Order Модель:**
   - Модель `Order`, объединяющая несколько `Item`.
   - Возможность оплаты всей суммы заказа через Stripe.
5. **Discount и Tax:**
   - Модели `Discount` и `Tax`, которые можно прикрепить к `Order`.
   - Корректное отображение скидок и налогов в Stripe Checkout.
6. **Мультивалютность:**
   - Добавить поле `Item.currency`.
   - Использовать разные Stripe Keypair для разных валют.
7. **Stripe Payment Intent:**
   - Реализовать оплату через Stripe Payment Intent вместо Stripe Session.

---


# Stripe Payment Integration Project

![Django](https://img.shields.io/badge/Django-1.0-blue)
![Stripe](https://img.shields.io/badge/Stripe-API-green)
![Docker](https://img.shields.io/badge/Docker-Ready-brightgreen)

## Описание

Этот проект представляет собой веб-приложение на Django с интеграцией платежной системы **Stripe**. Он позволяет создавать товары (`Item`), заказы (`Order`) с несколькими товарами, применять скидки (`Discount`) и налоги (`Tax`), а также обрабатывать платежи через Stripe API.

Проект использует следующие технологии:
- **Django**: Веб-фреймворк для создания backend-логики.
- **Stripe API**: Для обработки платежей.
- **Docker**: Для контейнеризации приложения.
- **REST Framework**: Для создания API.

---

## Функционал

### Основные возможности:
- **Товары (`Item`)**:
  - Создание и управление товарами с названием, описанием, ценой и валютой.
  - Просмотр детальной информации о товаре с кнопкой "Купить".

- **Заказы (`Order`)**:
  - Создание заказов с несколькими товарами.
  - Применение скидок и налогов к заказу.
  - Выполнение платежей через Stripe Payment Intent или Checkout Session.

- **Скидки (`Discount`)**:
  - Создание купонов со скидкой в процентах или фиксированной сумме.
  - Настройка длительности действия скидки (forever, once, repeating).

- **Налоги (`Tax`)**:
  - Добавление налогов к заказам.

- **API**:
  - REST API для управления товарами, заказами, скидками и налогами.
  - Интеграция с Stripe для создания платежных сессий.

- **Админ-панель**:
  - Полный контроль над моделями через Django Admin.

---

## Требования

Для запуска проекта вам понадобятся следующие инструменты:
- **Python 3.9+**
- **Docker**
- **Docker Compose**

---

## Развертывание через Docker

### 1. Клонирование репозитория

Склонируйте репозиторий проекта:

```bash
git clone https://github.com/Ziltriz/smart.git
cd smart/srtipedjango
```

### 2. Настройка переменных окружения

Создайте файл `.env` в корне проекта и добавьте необходимые переменные:

```env
# Stripe Keys
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Django Settings
DEBUG=True
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=*

# Database
POSTGRES_DB=stripe_payment
POSTGRES_USER=stripe_user
POSTGRES_PASSWORD=stripe_password
```

### 3. Запуск приложения

Используйте `docker-compose` для запуска приложения:

```bash
docker-compose up --build
```

Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000).

---

### 4. Создание миграций и суперпользователя

Подключитесь к контейнеру Django:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Создайте суперпользователя для доступа к админ-панели.

---

### 5. Админ-панель

Админ-панель доступна по адресу: [http://localhost:8000/admin](http://localhost:8000/admin).

Войдите с учетными данными суперпользователя, чтобы управлять товарами, заказами, скидками и налогами.

---

## API Endpoints

### Товары

- **GET `/item/{id}/`**: Получить информацию о товаре и кнопку "Купить".
- **GET `/buy/{id}/`**: Создать Checkout Session для оплаты товара.

### Заказы

- **GET `/order/{id}/`**: Получить информацию о заказе и кнопку "Оплатить".
- **GET `/api/create-payment-intent/{order_id}/`**: Создать Payment Intent для заказа.

---

## Тестирование платежей

Для тестирования платежей используйте тестовые данные Stripe:

- Номер карты: `4242 4242 4242 4242`
- Месяц/год: любая будущая дата
- CVV: `123`

---

## Дополнительные возможности

- **Логирование**: Все ошибки Stripe логируются в консоль.
- **Масштабируемость**: Приложение можно легко масштабировать, добавляя больше контейнеров через Docker Compose.
- **Безопасность**: Используется HTTPS для live-окружения.

---

## Авторы

- **Ziltriz**: [Ваш GitHub](https://github.com/Ziltriz)
