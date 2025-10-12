from telegram import Update
from telegram.ext import ContextTypes
from handlers.options.registration import user_state
from db.queries_users import user_exists, get_user_role
from texts.start import ALREADY_REGISTERED, START_MESSAGE
from keyboards.menu import STUDENT_MENU, TEACHER_MENU

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        role = get_user_role(chat_id)

        if role == "student":
            menu = STUDENT_MENU
        else:
            menu = TEACHER_MENU

        await update.message.reply_text(
            ALREADY_REGISTERED, 
            reply_markup=menu
        )
        return
    
    user_state[chat_id] = "awaiting_name"
    await update.message.reply_text(START_MESSAGE) 