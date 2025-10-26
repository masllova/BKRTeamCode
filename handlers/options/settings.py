from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from db.queries_users import get_user_by_chat_id, update_user_info
from texts.settings import (
    SELECT_UNIVERSITY_STUDENT, SELECT_UNIVERSITY_TEACHER, FACULTY_TEXT,
    SPECIALTY_TEXT, DEPARTMENT_TEXT, ARTICLES_TEXT, RESEARCH_INTERESTS_TEXT,
    DEGREE_TEXT, SELECT_STAGE_STUDENT, SELECT_STAGE_TEACHER, EMAIL_TEXT, 
    SUCCESS_TEXT
)
from keyboards.settings import make_student_settings_keyboard, make_teacher_settings_keyboard, SELECT_SETTINGS_KEYBOARD
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

    if data == "settings":
        await update.message.reply_text("Выберите раздел настроек", reply_markup=SELECT_SETTINGS_KEYBOARD)
    if data == "notification":
        return
    if data == "profile":
        user_data = get_user_by_chat_id(chat_id)
        text = "Здесь Вы можете редактировать свой профиль\n\nАктуальная информация:"

        has_faculty = False
        has_department = False
        has_specialty = False
        has_degree = False
        has_articles = False
        has_interests = False
        has_email = False

        if user_data["role"] == "student":
            text += f"\nСтупень образования: {user_data["stage"]}"
            text += f"\nУчебное заведение: {user_data["university"]}"
            faculty = user_data["faculty"]

            if faculty:
                has_faculty = True
                text += f"\nФакультет: {faculty}"
            department = user_data["department"]

            if department:
                has_department = True
                text += f"\nКафедра/Направление: {department}"
            specialty = user_data["specialty"]
            
            if specialty:
                has_specialty = True
                text += f"\nСпециальность: {user_data["specialty"]}"
        else:
            text += f"\nДолжность: {user_data["stage"]}"
            text += f"\nНаучное учреждение: {user_data["university"]}"
            degree = user_data["degree"]

            if degree:
                has_degree = True
                text += f"\nСтепень: {degree}"
        articles = user_data["articles"]

        if articles:
            has_articles = True
            text += f"\nСтатьи: {articles}"
        research_interests = user_data["research_interests"]
        
        if research_interests:
            has_interests = True
            text += f"\Научные интересы: {research_interests}"
        email = user_data["email"]
        
        if email:
            has_email = True
            text += f"\Почта: {email}"

        if user_data["role"] == "student":
            keyboard = make_student_settings_keyboard(has_faculty, has_department, has_specialty, has_articles, has_interests, has_email)
        else:
            keyboard = make_teacher_settings_keyboard(has_degree, has_articles, has_interests, has_email)
        await update.message.reply_text(text, reply_markup = keyboard)
    elif data == "student_stage":
        # 
        await update.message.reply_text(SELECT_STAGE_STUDENT, reply_markup=STUDENT_STAGES)
    elif data == "teacher_stage":
        # 
        await update.message.reply_text(SELECT_STAGE_TEACHER, reply_markup=TEACHER_STAGES)
    elif data == "student_university":
        settings_state[chat_id] = "student_university"
        await query.message.reply_text(SELECT_UNIVERSITY_STUDENT)
    elif data == "teacher_university":
        settings_state[chat_id] = "teacher_university"
        await query.message.reply_text(SELECT_UNIVERSITY_TEACHER)
    elif data == "student_faculty":
        settings_state[chat_id] = "student_faculty"
        await query.message.reply_text(FACULTY_TEXT)
    elif data == "student_department":
        settings_state[chat_id] = "student_department"
        await query.message.reply_text(DEPARTMENT_TEXT)
    elif data == "student_specialty":
        settings_state[chat_id] = "student_specialty"
        await query.message.reply_text(SPECIALTY_TEXT)
    elif data == "teacher_degree":
        settings_state[chat_id] = "teacher_degree"
        await query.message.reply_text(DEGREE_TEXT)
    elif data == "articles":
        settings_state[chat_id] = "articles"
        await query.message.reply_text(ARTICLES_TEXT)
    elif data == "research_interests":
        settings_state[chat_id] = "research_interests"
        await query.message.reply_text(RESEARCH_INTERESTS_TEXT)
    elif data == "email":
        settings_state[chat_id] = "email"
        await query.message.reply_text(EMAIL_TEXT)