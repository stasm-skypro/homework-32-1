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

#### Установка подписки

Команда:    
```POST``` ```http://127.0.0.1:8000/subscription/```

Тело запроса:
```json
{
    "course_id": 1      
}
```

Ответ:
```json
{
    "message": "Подписка добавлена"
}
```

## 3. Пагинация

По умолчаню пагинация имеет такие настройки:
- Количество элементов на одной странице - 2
- Максимальное количество элементов на одной странице - 10

#### Просмотр списка курсов

Команда:
```GET``` ```http://127.0.0.1:8000/course/```

Ответ:
```json
{
    "count": 13,
    "next": "http://127.0.0.1:8000/course/?page=2",
    "previous": null,
    "results": [
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
        }
    ]
}
```

#### Просмотр курса - установим page_size = 3

Команда:
```GET``` ```http://127.0.0.1:8000/course/?page_size=3```

Ответ:    
```json
{
    "count": 13,
    "next": "http://127.0.0.1:8000/course/?page=2&page_size=3",
    "previous": null,
    "results": [
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
        {
            "id": 3,
            "name": "SQL для начинающих",
            "description": "Основы работы с базами данных.",
            "lessons_count": 1,
            "is_subscribed": false
        }
    ]
}
```

#### Просмотр урокова - установим page_size = 3

Команда:
```GET``` ```http://127.0.0.1:8000/lesson/list/?page=1&page_size=3```

Ответ:
```json
{
    "count": 5,
    "next": "http://127.0.0.1:8000/lesson/list/?page=2&page_size=3",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Введение в Python",
            "description": "История и применение Python.",
            "image": "http://127.0.0.1:8000/media/lessons/python_intro.jpg",
            "video": "http://127.0.0.1:8000/media/lessons/python_intro.mp4",
            "course": 1,
            "owner": null
        },
        {
            "id": 2,
            "name": "Переменные и типы данных",
            "description": "Разбор переменных и основных типов данных.",
            "image": "http://127.0.0.1:8000/media/lessons/python_vars.jpg",
            "video": "http://127.0.0.1:8000/media/lessons/python_vars.mp4",
            "course": 1,
            "owner": null
        },
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

## 4. Тестирование

Для тестирования контроллеров используется `rest_framework test`.
Тесты написаны для CRUD-операций с уроками и контроллером подписки.

Результат покрытия тестами сохранён в `htmlcov`.


## 5. Дополнительное задание

### Тесты для контроллера Курса.

#### Объяснение тестов:
Создание курса (POST /courses/) 

Владельцем (✅ 201)

Неавторизованным пользователем (❌ 401)

Получение списка курсов (GET /courses/) 

Авторизованным пользователем (✅ 200)

Неавторизованным пользователем (❌ 401)

Просмотр курса (GET /courses/{id}/)

Владельцем (✅ 200)

Модератором (✅ 200)

Посторонним пользователем (❌ 403)

Обновление курса (PUT /courses/{id}/)

Владельцем (✅ 200)

Модератором (✅ 200)

Посторонним пользователем (❌ 403)

Удаление курса (DELETE /courses/{id}/)

Владельцем (✅ 204)

Модератором (❌ 403)

### Тесты для контроллера Пользователя.

Написаны тесты для контроллера Пользователя.
Проверяют основные CRUD-операции UserViewSet, а также учитывает права доступа, предотвращая возможность редактирования и удаления чужих профилей.
