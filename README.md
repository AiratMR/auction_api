# Auction API

## Установка
1. Клонировать репозиторий: git clone https://github.com/AiratMR/auction_api.git
2. Установить Docker и docker-compose.
3. В файле config/settings.py установить значения настроек электронной почты:

```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yourmail@mail.ru'
EMAIL_HOST_PASSWORD = 'password'
```

## Запуск

Выполнить команду: docker-compose up

## Документация

Документация доступна после запуска приложения по ссылкам:
  1. http://localhost/swagger.json
  2. http://localhost/swagger.yaml
  3. http://localhost/swagger/
  4. http://localhost/redoc/
