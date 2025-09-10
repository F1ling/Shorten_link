##Shorten_link

---
Сервис для сокращения длинных URL-адресов с автоматическим переходом по короткой ссылке.

# Установка и запуск

1. Клонируйте репозиторий:
```bash
    git clone <repository-url>
    cd shortener-service
```
2. Создайте виртуальное окружение и активируйте его:
```bash
    python -m venv venv
    source venv/bin/activate  # для Linux/Mac
    # или
    venv\Scripts\activate  # для Windows
```    
3.Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Запустите приложение:
```bash
    cd app
    uvicorn main:app --reload
```
5.Откройте браузер и перейдите по адресу: http://localhost:8000

# API endpoints

POST /shorten - создание короткой ссылки

GET /{short_code} - перенаправление по короткой ссылке

GET / - главная страница с формой

# Особенности

Ссылки хранятся в течение 24 часов

Автоматический редирект при переходе по короткой ссылке

Валидация URL

Минимальный веб-интерфейс 
