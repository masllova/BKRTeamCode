from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menu import BUTTON_TO_COMMAND, get_menu_keyboard
from db.queries_users import user_exists, get_user_role
from texts.menu import MENU_AVAILABLE, NOT_REGISTERED, MENU_RESPONSES
from handlers.options.search import search_state

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        role = get_user_role(chat_id)
        keyboard = get_menu_keyboard(role)

        await update.message.reply_text(
            MENU_AVAILABLE,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(NOT_REGISTERED)

async def handle_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    command = BUTTON_TO_COMMAND.get(text, "unknown")

    chat_id = update.message.chat_id
    search_state.pop(chat_id, None)

    if command == "search":
        await open_search(update)
        return

    response = MENU_RESPONSES.get(command, MENU_RESPONSES["unknown"])
    await update.message.reply_text(response)

async def open_search(update: Update):
    chat_id = update.message.chat_id
    search_state[chat_id] = {
        "query": None,
        "last_id": None,
        "target_role": None
    }
    await update.message.reply_text("🔍 Введите текст для поиска пользователей:")
    return