from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menu import STUDENT_MENU_BUTTONS, TEACHER_MENU_BUTTONS
from handlers.options.registration import handle_registration_text, user_state
from handlers.options.menu import handle_menu_text, menu_state
from handlers.options.search import handle_search_text

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text

    if chat_id in user_state:
        await handle_registration_text(update, context)
        return
    
    print(menu_state)

    if menu_state.get(chat_id) == "awaiting_search_query":
        await handle_search_text(update, context)
        return

    all_buttons = STUDENT_MENU_BUTTONS + TEACHER_MENU_BUTTONS
    if text in all_buttons:
        await handle_menu_text(update, context)
        return

    # Если ничего не подошло
    await update.message.reply_text("❗ Неизвестная команда. Пожалуйста, используйте кнопки меню.")