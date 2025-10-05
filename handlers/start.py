from telegram import Update
from telegram.ext import ContextTypes
from handlers.registration import user_state
from db.queries_users import user_exists
from texts.start import ALREADY_REGISTERED, START_MESSAGE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        await update.message.reply_text(ALREADY_REGISTERED)
        return
    
    user_state[chat_id] = "awaiting_name"
    await update.message.reply_text(START_MESSAGE) 