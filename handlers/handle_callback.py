from telegram import Update
from telegram.ext import ContextTypes
from db.queries_users import get_user_by_chat_id
from handlers.options.registration import handle_registration_callback, user_state
from handlers.options.search import handle_search_callback, search_state
from handlers.options.requests import handle_requests_callback, requests_state
from handlers.options.projects import handle_projects_callback, groups_state
from handlers.options.settings import handle_settings_callback, settings_state
from texts.options import NOT_REGISTERED

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id
    user = get_user_by_chat_id(chat_id)

    print(user_state)

    if not user:
        if chat_id in user_state:
            await handle_registration_callback(update, context)
            return
        else:
            await query.message.reply_text(NOT_REGISTERED)
            return
    elif search_state.get(chat_id):
        await handle_search_callback(update, context)
        return
    elif requests_state.get(chat_id):
        await handle_requests_callback(update, context)
        return
    elif groups_state.get(chat_id):
        await handle_projects_callback(update, context)
        return
    elif settings_state.get(chat_id):
        await handle_settings_callback(update, context)
        return