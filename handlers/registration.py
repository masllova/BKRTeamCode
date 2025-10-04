from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_users import add_user, user_exists
from texts.registration import (
    ALREADY_REGISTERED,
    REGISTRATION_SUCCESS,
    SELECT_ROLE,
    SELECT_ROLE_BY_BUTTONS
)
from keyboards.registration import ROLE_KEYBOARD

user_state = {}
user_data_temp = {}
ROLE_MAPPING = {
    "студент": "student",
    "преподаватель": "teacher"
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip().lower()

    if user_exists(chat_id):
        await update.message.reply_text(ALREADY_REGISTERED)
        return

    if user_state.get(chat_id) == "awaiting_name":
        full_name = text
        user_data_temp[chat_id] = {"full_name": full_name}
        user_state[chat_id] = "awaiting_role"

        await update.message.reply_text(SELECT_ROLE, reply_markup=ROLE_KEYBOARD)
        return

    if user_state.get(chat_id) == "awaiting_role":
        if text in ROLE_MAPPING:
            role_key = ROLE_MAPPING[text]
            full_name = user_data_temp[chat_id]["full_name"]

            add_user(chat_id, full_name, role_key)
            user_state.pop(chat_id, None)
            user_data_temp.pop(chat_id, None)

            await update.message.reply_text(
                REGISTRATION_SUCCESS.format(full_name=full_name)
            )
            print(f"✔️ Сохранили пользователя: {full_name} "
                  f"(telegram_id={chat_id}, role={role_key})")
        else:
            await update.message.reply_text(SELECT_ROLE_BY_BUTTONS, reply_markup=ROLE_KEYBOARD)