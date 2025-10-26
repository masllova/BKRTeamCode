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
from keyboards.settings import (
    make_student_settings_keyboard, make_teacher_settings_keyboard, 
    make_back_keyboard, SELECT_SETTINGS_KEYBOARD
)
from keyboards.stage import STUDENT_STAGES, TEACHER_STAGES
from texts.stage import TEACHER_STAGE_NAMES, STUDENT_STAGE_NAMES

settings_state = {}

async def handle_settings_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    state = settings_state.get(chat_id)

    if state == "stage":
        # TO DO
        return
    elif state == "university":
        update_user_info(chat_id, "university", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "faculty":
        update_user_info(chat_id, "faculty", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "university":
        update_user_info(chat_id, "university", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "department":
        update_user_info(chat_id, "department", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "specialty":
        update_user_info(chat_id, "specialty", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "degree":
        update_user_info(chat_id, "degree", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "articles":
        update_user_info(chat_id, "articles", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "research_interests":
        update_user_info(chat_id, "research_interests", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif state == "email":
        update_user_info(chat_id, "email", text)
        await update.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
                                        

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    data = query.data
    state = settings_state.get(chat_id)

    if data == "settings":
        await query.message.reply_text("Выберите раздел настроек", reply_markup=SELECT_SETTINGS_KEYBOARD)
    elif data == "notification":
        return
    elif data == "profile":
        user_data = get_user_by_chat_id(chat_id)
        text = "Здесь вы можете редактировать свой профиль\n\nАктуальная информация:\n"

        has_faculty = False
        has_department = False
        has_specialty = False
        has_degree = False
        has_articles = False
        has_interests = False
        has_email = False

        if user_data["role"] == "student":
            stage = user_data["stage"]
            if stage and stage.strip():
                stage_key = stage.strip()
                stage_name = STUDENT_STAGE_NAMES.get(stage_key, stage_key)

                text += f"\nСтупень образования: {stage_name}"
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
            stage = user_data["stage"]
            if stage and stage.strip():
                stage_key = stage.strip()
                stage_name = TEACHER_STAGE_NAMES.get(stage_key, stage_key)

                text += f"\nДолжность: {stage_name}"
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
            text += f"\nНаучные интересы: {research_interests}"
        email = user_data["email"]
        
        if email:
            has_email = True
            text += f"\nПочта: {email}"

        if user_data["role"] == "student":
            keyboard = make_student_settings_keyboard(has_faculty, has_department, has_specialty, has_articles, has_interests, has_email)
        else:
            keyboard = make_teacher_settings_keyboard(has_degree, has_articles, has_interests, has_email)
        await query.message.reply_text(text, reply_markup = keyboard)
    elif state == "stage":
        update_user_info(chat_id, "stage", text)
        await query.message.reply_text(SUCCESS_TEXT, reply_markup = make_back_keyboard("profile"))
    elif data == "student_stage":
        settings_state[chat_id] = "stage"
        await query.message.reply_text(SELECT_STAGE_STUDENT, reply_markup=STUDENT_STAGES)
    elif data == "teacher_stage":
        settings_state[chat_id] = "stage"
        await query.message.reply_text(SELECT_STAGE_TEACHER, reply_markup=TEACHER_STAGES)
    elif data == "student_university":
        settings_state[chat_id] = "university"
        await query.message.reply_text(SELECT_UNIVERSITY_STUDENT)
    elif data == "teacher_university":
        settings_state[chat_id] = "university"
        await query.message.reply_text(SELECT_UNIVERSITY_TEACHER)
    elif data == "student_faculty":
        settings_state[chat_id] = "faculty"
        await query.message.reply_text(FACULTY_TEXT)
    elif data == "student_department":
        settings_state[chat_id] = "department"
        await query.message.reply_text(DEPARTMENT_TEXT)
    elif data == "student_specialty":
        settings_state[chat_id] = "specialty"
        await query.message.reply_text(SPECIALTY_TEXT)
    elif data == "teacher_degree":
        settings_state[chat_id] = "degree"
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