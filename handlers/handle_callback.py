from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import get_user_by_chat_id
from handlers.options.registration import handle_registration_callback, user_state


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user = get_user_by_chat_id(chat_id)

    if user:
        # to do
        return

    if chat_id in user_state:
        await handle_registration_callback(update, context)
        return
    
    await query.message.reply_text("❗ Пожалуйста, пройдите регистрацию с начала: /start")