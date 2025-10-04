from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import add_user, user_exists
from texts.registration import ALREADY_REGISTERED, REGISTRATION_SUCCESS

# Простое состояние (пока без Redis или БД)
user_state = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if user_exists(chat_id):
        await update.message.reply_text(ALREADY_REGISTERED)
        return

    if user_state.get(chat_id) == "awaiting_name":
        full_name = text
        role = "студент"  # пока по умолчанию

        add_user(chat_id, full_name, role)
        user_state.pop(chat_id, None)

        await update.message.reply_text(REGISTRATION_SUCCESS.format(full_name=full_name))
        print(f"✔️ Сохранили пользователя: {full_name} (telegram_id={chat_id}, role={role})")