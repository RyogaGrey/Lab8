# OTPRO Lab 8

Telegram Bot для отправки Email через SMTP
Бот запрашивает у пользователя email-адрес и текст сообщения, а затем отправляет письмо на указанный адрес.

Установка и настройка
---
1. Клонирование репозитория
```bash
  git clone https://github.com/ваш-аккаунт/telegram-smtp-bot.git
  cd telegram-smtp-bot
```

2. Создание виртуального окружения
```bash
  python -m venv .venv
  source .venv/bin/activate  # Для Linux/Mac
  .venv\Scripts\activate     # Для Windows
```
3. Установка зависимостей
```bash
  pip install -r requirements.txt
```
4. Настройка переменных окружения
Создайте файл .env в корневой директории и добавьте свои данные:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_бота
EMAIL=ваша_почта@сервер.ru
MAIL_PASSWORD=пароль_приложения
```
TELEGRAM_BOT_TOKEN: Токен, полученный у BotFather.
EMAIL: Ваш email на Яндексе (например, example@yandex.ru).
MAIL_PASSWORD: Пароль приложения, например, созданный в настройках Яндекс.Почты.
