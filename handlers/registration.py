from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import add_user, user_exists
from keyboards.registration import ROLE_KEYBOARD
from keyboards.stage import STUDENT_STAGES, TEACHER_STAGES
from texts.registration import (
    ALREADY_REGISTERED,
    SELECT_ROLE,
    SELECT_UNIVERSITY_STUDENT,
    SELECT_UNIVERSITY_TEACHER,
    SELECT_STAGE_STUDENT,
    SELECT_STAGE_TEACHER,
    REGISTRATTION_ERROR,
    REGISTRATION_SUCCESS
)

user_state = {}
user_data_temp = {}

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    state = user_state.get(chat_id)

    if state == "awaiting_name":
        if user_exists(chat_id):
            await update.message.reply_text(ALREADY_REGISTERED)
            return
        user_data_temp[chat_id] = {"full_name": text}
        user_state[chat_id] = "awaiting_role"
        await update.message.reply_text(SELECT_ROLE, reply_markup=ROLE_KEYBOARD)

    elif state == "awaiting_university":
        if chat_id not in user_data_temp or "role" not in user_data_temp[chat_id]:
            await update.message.reply_text(REGISTRATTION_ERROR)
            user_state.pop(chat_id, None)
            user_data_temp.pop(chat_id, None)
            return
        user_data_temp[chat_id]["university"] = text
        role_key = user_data_temp[chat_id]["role"]
        user_state[chat_id] = "awaiting_stage"

        if role_key == "student":
            await update.message.reply_text(SELECT_STAGE_STUDENT, reply_markup=STUDENT_STAGES)
        else:
            await update.message.reply_text(SELECT_STAGE_TEACHER, reply_markup=TEACHER_STAGES)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data
    state = user_state.get(chat_id)

    if state == "awaiting_role":
        user_data_temp[chat_id]["role"] = data
        user_state[chat_id] = "awaiting_university"

        if data == "student":
            text = SELECT_UNIVERSITY_STUDENT
        else:
            text = SELECT_UNIVERSITY_TEACHER

        await query.message.reply_text(text)

    elif state == "awaiting_stage":
        full_name = user_data_temp[chat_id]["full_name"]
        role_key = user_data_temp[chat_id]["role"]
        university = user_data_temp[chat_id]["university"]
        stage = data

        add_user(chat_id, full_name, role_key, university, stage)

        user_state.pop(chat_id, None)
        user_data_temp.pop(chat_id, None)

        await query.message.reply_text(
            REGISTRATION_SUCCESS.format(full_name=full_name)
        )
        print(f"✔️ Сохранили пользователя: {full_name}, role={role_key}, "
              f"university={university}, stage={stage}")