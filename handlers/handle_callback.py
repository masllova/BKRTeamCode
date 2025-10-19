from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import get_user_by_chat_id
from handlers.options.registration import handle_registration_callback, user_state
from handlers.options.search import handle_search_callback, search_state
from texts.options import NOT_REGISTERED

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    # data = query.data

    if chat_id in user_state:
        await handle_registration_callback(update, context)
        return

    user = get_user_by_chat_id(chat_id)
    if not user:
        await query.message.reply_text(NOT_REGISTERED)
        return

    if search_state.get(chat_id):
        await handle_search_callback(update, context)
        return