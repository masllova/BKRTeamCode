from telegram import Update
from telegram.ext import ContextTypes
from handlers.options.registration import user_state
from db.queries_users import user_exists, get_user_role
from texts.start import ALREADY_REGISTERED, START_MESSAGE
from keyboards.menu import get_menu_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        role = get_user_role(chat_id)
        keyboard = get_menu_keyboard(role)

        await update.message.reply_text(
            ALREADY_REGISTERED, 
            reply_markup=keyboard
        )
        return
    
    user_state[chat_id] = "awaiting_name"
    await update.message.reply_text(START_MESSAGE) 