import re
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
import asyncio

# Загрузка переменных окружения из .env файла
load_dotenv(dotenv_path=".env")  # Явно указываем путь

# Получение значений из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
EMAIL = os.getenv("EMAIL")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()

# Создание кнопки "Начать" для запуска бота
start_button = KeyboardButton(text="Начать")
start_keyboard = ReplyKeyboardMarkup(
    keyboard=[[start_button]],
    resize_keyboard=True,  # Уменьшает размер кнопок
    one_time_keyboard=True  # Скрывает клавиатуру после нажатия
)

# Функция для отправки email через SMTP Яндекса
async def send_email(smtp_server, smtp_port, email, password, recipient, message):
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = recipient
    msg["Subject"] = "Сообщение от Telegram-бота"
    msg.attach(MIMEText(message, "plain", "utf-8"))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(email, password)  # Передача логина и пароля
            server.sendmail(email, recipient, msg.as_string())
        return "Сообщение успешно отправлено!"
    except smtplib.SMTPException as e:
        return f"Ошибка при отправке сообщения: {e}"

# Хранилище для временного хранения email пользователя
user_data = {}

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Здравствуйте! Пожалуйста, введите ваш email:", reply_markup=start_keyboard)
    user_data[message.from_user.id] = {"email": None}  # Инициализация данных пользователя

# Обработчик для нажатия кнопки "Начать"
@router.message(lambda msg: msg.text == "Начать")
async def start_via_button(message: Message):
    await start_handler(message)  # Перенаправляем в обработчик /start

# Обработчик для проверки email
@router.message(lambda msg: re.match(r"[^@]+@[^@]+\.[^@]+", msg.text.strip()))
async def email_handler(message: Message):
    email = message.text.strip()
    user_data[message.from_user.id]["email"] = email
    await message.answer(f"Спасибо! Теперь отправьте текст сообщения, которое вы хотите отправить на {email}.")

# Обработчик текста сообщения и отправка email
@router.message()
async def message_handler(message: Message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id]["email"]:
        recipient = user_data[user_id]["email"]
        text_message = message.text.strip()

        # Отправка email через SMTP Яндекса
        result = await send_email("smtp.yandex.ru", 465, EMAIL, MAIL_PASSWORD, recipient, text_message)
        await message.answer(result)

        # Сброс email пользователя для возможности ввода нового
        user_data[user_id]["email"] = None
        await message.answer("Можете отправить новый email или использовать команду /start.", reply_markup=start_keyboard)
    else:
        await message.answer("Пожалуйста, введите корректный email сначала.")

# Подключаем маршрутизатор к диспетчеру
dp.include_router(router)

# Основной запуск бота
async def main():
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
