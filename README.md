# NoteApp

## Запуск приложения
    Создать .env файл и скопировать в него содержимое из .env.example
### Запустить команду: <br>
    docker compose -f docker_compose/app.yaml up --build -d

## Запуск тестов
### Зайти в запущенный контейнер <br>
    docker exec -it note_app bash
### Запустить тесты внутри контейнера <br>
    pytest

## Примеры запросов
### Регистрация <br>
#### Запрос <br>
    curl -X 'POST' \
      'http://127.0.0.1:8000/users/register' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "ivanovivan2000@mail.ru",
      "password": "string"
    }'
#### Ответ
    {
      "id": "15457cb6-d99e-497e-8e8f-b4ec2a8a658e",
      "email": "ivanovivan2000@mail.ru",
      "created_at": "2024-08-28T17:29:06.536318"
    }
### Аутентификация для получения токена
#### Запрос
    curl -X 'POST' \
      'http://127.0.0.1:8000/auth/login' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'grant_type=password&username=ivanovivan2000%40mail.ru&password=string&scope=&client_id=string&client_secret=string'
#### Ответ
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Iml2YW5vdml2YW4yMDAwQG1haWwucnUiLCJleHAiOjE3MjQ4NjgxMTl9.FUj22VGZxxzsKHN7piFnE0HkFL3goo01wADhY8U1MME",
      "token_type": "bearer"
    }
### Создание заметки
#### Запрос
    curl -X 'POST' \
      'http://127.0.0.1:8000/notes' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Iml2YW5vdml2YW4yMDAwQG1haWwucnUiLCJleHAiOjE3MjQ4Njg4NDh9.BnewW0zHCFyWg_fiX4ftrLGhFROKZ7F3Cneara9jqRE' \
      -H 'Content-Type: application/json' \
      -d '{
      "text": "Выпалнить зодание до пятныцы"
    }'

#### Ответ
    {
      "id": "eafb6913-f4c6-4409-ab0c-87f3ae41a4a5",
      "text": "Выполнить задание до пятницы",
      "owner_id": "15457cb6-d99e-497e-8e8f-b4ec2a8a658e",
      "created_at": "2024-08-28T17:44:55.391148"
    }
### Получение все заметок авторизованного пользователя
#### Запрос
    curl -X 'GET' \
      'http://127.0.0.1:8000/notes?limit=10&offset=0' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Iml2YW5vdml2YW4yMDAwQG1haWwucnUiLCJleHAiOjE3MjQ4Njg4NDh9.BnewW0zHCFyWg_fiX4ftrLGhFROKZ7F3Cneara9jqRE'
#### Ответ
    {
      "offset": 0,
      "limit": 10,
      "items": [
        {
          "id": "b01ae075-c10b-4c4b-b351-93e130de734f",
          "text": "привет это тест",
          "owner_id": "15457cb6-d99e-497e-8e8f-b4ec2a8a658e",
          "created_at": "2024-08-28T17:44:10.894237"
        },
        {
          "id": "eafb6913-f4c6-4409-ab0c-87f3ae41a4a5",
          "text": "Выполнить задание до пятницы",
          "owner_id": "15457cb6-d99e-497e-8e8f-b4ec2a8a658e",
          "created_at": "2024-08-28T17:44:55.391148"
        }
      ]
    }
### Тестирование в postman
https://web.postman.co/workspace/a1ea1356-c5f9-4f94-8c01-4c3b4aa64274/request/27815345-4b041c91-d040-481a-8f33-e6fae4ed59a3
