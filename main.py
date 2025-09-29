import os
import psycopg2
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Переменные окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
DB_PASSWORD = os.getenv("VKR_DB_PASSWORD")
DB_NAME = "vkrbot_db"
DB_USER = "vkrbot_user"
DB_HOST = "localhost"

# Подключение к базе
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()

# Состояние пользователя
user_state = {}

# Хэндлеры бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_state[chat_id] = "awaiting_name"
    await update.message.reply_text("Привет! Я VKRTeamBot. Введи своё ФИО:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if user_state.get(chat_id) == "awaiting_name":
        full_name = text
        role = "студент"  # по умолчанию, позже надо менять

        cursor.execute(
            """
            INSERT INTO users (telegram_id, full_name, role)
            VALUES (%s, %s, %s)
            ON CONFLICT (telegram_id) DO NOTHING;
            """,
            (chat_id, full_name, role)
        )
        conn.commit()
        user_state.pop(chat_id)

        await update.message.reply_text(f"Привет, {full_name}!")
        print(f"✔️ Сохранили пользователя: {full_name} (telegram_id={chat_id}, role={role})")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Бот запущен...")
    app.run_polling()