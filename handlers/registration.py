from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import add_user, user_exists
from db.queries_users import get_user_role
from texts.registration import (
    ALREADY_REGISTERED,
    SELECT_ROLE,
    SELECT_UNIVERSITY_STUDENT,
    SELECT_UNIVERSITY_TEACHER,
    REGISTRATION_SUCCESS
)
from keyboards.registration import ROLE_KEYBOARD

user_state = {}
user_data_temp = {}

async def handle_name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if user_exists(chat_id):
        await update.message.reply_text(ALREADY_REGISTERED)
        return

    if user_state.get(chat_id) != "awaiting_role":
        user_data_temp[chat_id] = {"full_name": text}
        user_state[chat_id] = "awaiting_role"

        await update.message.reply_text(SELECT_ROLE, reply_markup=ROLE_KEYBOARD)
        return

async def handle_role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    role_key = query.data  # "student" or "teacher"

    user_data_temp[chat_id]["role"] = role_key
    user_state[chat_id] = "awaiting_university"

    if role_key == "student":
        text = SELECT_UNIVERSITY_STUDENT
    else:
        text = SELECT_UNIVERSITY_TEACHER

    await query.message.reply_text(text)

async def handle_university_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if user_state.get(chat_id) != "awaiting_university":
        return

    full_name = user_data_temp[chat_id]["full_name"]
    role_key = user_data_temp[chat_id]["role"]
    university = text

    add_user(chat_id, full_name, role_key, university)

    user_state.pop(chat_id, None)
    user_data_temp.pop(chat_id, None)

    await update.message.reply_text(
        REGISTRATION_SUCCESS.format(full_name=full_name)
    )
    print(f"✔️ Сохранили пользователя: {full_name}, role={role_key}, university={university}")