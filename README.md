# Социальная сеть для обмена фотографиями

Backend приложение для социальной сети, разработанное на Django REST Framework.

## Описание проекта

API для социальной сети, позволяющее пользователям:
- Создавать публикации с текстом и фотографиями
- Комментировать публикации
- Ставить лайки
- Редактировать свои публикации

## Технологии

- Python 3.x
- Django 5.0.2
- Django REST Framework
- PostgreSQL
- Pillow (для работы с изображениями)

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/pahankov/diplom.git
cd diplom
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте базу данных PostgreSQL:
```sql
CREATE DATABASE social_network;
```

5. Настройте подключение к базе данных в файле `social_network/local_settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'social_network',
        'USER': 'postgres',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

6. Примените миграции:
```bash
python manage.py migrate
```

7. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

8. Запустите сервер разработки:
```bash
python manage.py runserver
```

## API Endpoints

### Аутентификация
- `POST /api-token-auth/` - получение токена авторизации

### Публикации
- `GET /api/posts/` - список всех публикаций
- `POST /api/posts/` - создание новой публикации
- `GET /api/posts/{id}/` - получение деталей публикации
- `PUT /api/posts/{id}/` - обновление публикации
- `DELETE /api/posts/{id}/` - удаление публикации
- `POST /api/posts/{id}/like/` - поставить/убрать лайк

### Комментарии
- `GET /api/posts/{post_id}/comments/` - список комментариев к публикации
- `POST /api/posts/{post_id}/comments/` - создание комментария
- `GET /api/posts/{post_id}/comments/{id}/` - получение комментария
- `PUT /api/posts/{post_id}/comments/{id}/` - обновление комментария
- `DELETE /api/posts/{post_id}/comments/{id}/` - удаление комментария

### Пользователи
- `GET /api/users/` - список пользователей
- `GET /api/users/{id}/` - информация о пользователе

## Административная панель

Доступна по адресу `/admin/`. Используйте учетные данные суперпользователя для входа.

## Автор

Павел Ковалевский
