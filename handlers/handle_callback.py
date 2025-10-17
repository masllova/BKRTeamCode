from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import get_user_by_chat_id
from handlers.options.registration import handle_registration_callback, user_state
from handlers.options.search import handle_search_query_callback, handle_searching_results_callback, search_state

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
        await query.message.reply_text("❗ Пожалуйста, пройдите регистрацию с начала: /start")
        return

    state_info = search_state.get(chat_id, {})
    state = state_info.get("state")

    if state == "awaiting_search_query":
        await handle_search_query_callback(update, context)
        return

    elif state == "searching_results":
        await handle_searching_results_callback(update, context)
        return