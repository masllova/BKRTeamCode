from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import add_user, user_exists

# Простое состояние (пока без Redis или БД)
user_state = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if user_exists(chat_id):
        await update.message.reply_text("Ты уже зарегистрирован! Введи /menu для перехода в главное меню.")
        return

    if user_state.get(chat_id) == "awaiting_name":
        full_name = text
        role = "студент"  # пока по умолчанию

        add_user(chat_id, full_name, role)
        user_state.pop(chat_id, None)

        await update.message.reply_text(f"Привет, {full_name}!")
        print(f"✔️ Сохранили пользователя: {full_name} (telegram_id={chat_id}, role={role})")