# Домашняя работа к модулю 8
# Тема 32.1 Валидаторы, пагинация и тесты

## 1. Валидация курсов и уроков

Проверяем поля `description` моделей `Course` и `Lesson`. 
Если в описании есть ссылка на интернет-ресурс, проверяем, что ссылка является допустимой. Допустима ссылка только на `YouTube`.

#### Правильный запрос:
Команда:
```POST``` ```http://127.0.0.1:8000/course/```

Тело запроса:
```json
{
    "name": "Test course",
    "description": "Test course description."
}
```

Ответ:
```json
{
    "id": 16,
    "name": "Test course",
    "description": "Test course description.",
    "lessons_count": 0
}
```

#### Правильный запрос:
Команда:
```POST``` ```http://127.0.0.1:8000/course/```

Тело запроса:
```json 
{
    "name": "Test course",      
    "description": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"    
}
```

Ответ:
```json
{
    "id": 17,
    "name": "Test course 2",
    "description": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "lessons_count": 0
}
```

#### Запрос с ошибкой:
Команда:    
```POST``` ```http://127.0.0.1:8000/lesson/create/```

Тело запроса:
```json
{
    "name": "Test lesson",
    "description": "Test lesson https://yandex.kz",
    "image": null,
    "video": null,
    "course": 1
}
```

Ответ:
```json
{
 "non_field_errors": [
        "Ссылка на другие каналы кроме youtube не допустима."
    ]   
}
```

## 2. Модель подписки пользователя

Добавлена модель подписки на обновления курса для пользователя.

#### Просмотр списка курсов

Команда:
```GET``` ```http://127.0.0.1:8000/course/```

Ответ:
```json
[
   {
        "id": 1,
        "name": "Python для начинающих",
        "description": "Основы языка Python.",
        "lessons_count": 2,
        "is_subscribed": false
    },
    {
        "id": 2,
        "name": "Django с нуля",
        "description": "Создание веб-приложений на Django.",
        "lessons_count": 1,
        "is_subscribed": false
    },
  ...
]
``` 

#### Просмотр курса

Команда:    
```GET``` ```http://127.0.0.1:8000/course/2/```

Ответ:
```json
{
    "name": "Django с нуля",
    "description": "Создание веб-приложений на Django.",
    "lessons_count": 1,
    "lessons": [
        {
            "id": 3,
            "name": "Основы Django",
            "description": "Структура проекта Django.",
            "image": "http://127.0.0.1:8000/media/lessons/django_basics.jpg",
            "video": "http://127.0.0.1:8000/media/lessons/django_basics.mp4",
            "course": 2,
            "owner": null
        }
    ]
}
```

## 3. Пагинация

## 4. Тестирование
