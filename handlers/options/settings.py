from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.queries_users import get_user_by_chat_id
from texts.settings import (
    SELECT_UNIVERSITY_STUDENT, SELECT_UNIVERSITY_TEACHER, FACULTY_TEXT,
    SPECIALTY_TEXT, DEPARTMENT_TEXT, ARTICLES_TEXT, RESEARCH_INTERESTS_TEXT,
    DEGREE_TEXT, SELECT_STAGE_STUDENT, SELECT_STAGE_TEACHER, EMAIL_TEXT, 
    SUCCESS_TEXT, OLD_VALUE
)
from keyboards.stage import STUDENT_STAGES, TEACHER_STAGES

settings_state = {}

async def handle_settings_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    state = settings_state.get(chat_id)

    # TO DO
    return

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data

    if data == "student_stage":
        await update.message.reply_text(SELECT_STAGE_STUDENT, reply_markup=STUDENT_STAGES)
    elif data == "teacher_stage":
        await update.message.reply_text(SELECT_STAGE_TEACHER, reply_markup=TEACHER_STAGES)
    elif data == "student_university":
        settings_state[chat_id] = "student_university"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["university"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += SELECT_UNIVERSITY_STUDENT
        query.message.reply_text(text)
    elif data == "teacher_university":
        settings_state[chat_id] = "teacher_university"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["university"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += SELECT_UNIVERSITY_TEACHER
        query.message.reply_text(text)
    elif data == "student_faculty":
        settings_state[chat_id] = "student_faculty"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["faculty"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += FACULTY_TEXT
        query.message.reply_text(text)
    elif data == "student_department":
        settings_state[chat_id] = "student_department"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["department"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += DEPARTMENT_TEXT
        query.message.reply_text(text)
    elif data == "student_specialty":
        settings_state[chat_id] = "student_specialty"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["specialty"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += SPECIALTY_TEXT
        query.message.reply_text(text)
    elif data == "teacher_degree":
        settings_state[chat_id] = "teacher_degree"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["degree"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += DEGREE_TEXT
        query.message.reply_text(text)
    elif data == "articles":
        settings_state[chat_id] = "articles"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["articles"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += ARTICLES_TEXT
        query.message.reply_text(text)
    elif data == "research_interests":
        settings_state[chat_id] = "research_interests"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["research_interests"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += RESEARCH_INTERESTS_TEXT
        query.message.reply_text(text)
    elif data == "email":
        settings_state[chat_id] = "email"
        text = ""
        old_value = get_user_by_chat_id(chat_id)["email"]

        if old_value:
            text += OLD_VALUE.format(value=old_value)
        text += EMAIL_TEXT
        query.message.reply_text(text)

