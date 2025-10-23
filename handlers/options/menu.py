from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu import BUTTON_TO_COMMAND, get_menu_keyboard
from db.queries_users import user_exists, get_user_role, get_user_group_ids
from db.queries_groups import get_group_by_id
from texts.menu import MENU_AVAILABLE, NOT_REGISTERED, MENU_RESPONSES
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER
from handlers.options.search import search_state
from handlers.options.requests import requests_state
from handlers.options.projects import groups_state

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
    requests_state.pop(chat_id, None)
    groups_state.pop(chat_id, None)

    if command == "search":
        search_state[chat_id] = {
            "query": None,
            "last_id": None,
            "target_role": None
        }
        role = get_user_role(chat_id)

        if role == "student":
            await update.message.reply_text(SEARCH_TEACHER)
        else:
            await update.message.reply_text(SEARCH_STUDENT)
        return
    if command == "requests":
        requests_state[chat_id] = "awaiting_type"
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Входящие заявки", callback_data="incoming_requests")],
            [InlineKeyboardButton("Отправленные заявки", callback_data="outgoing_requests")]
        ])
        
        await update.message.reply_text(
            "Выберите, какие заявки хотите просмотреть:",
            reply_markup=keyboard
        )
        return
    
    if command == "projects":
        groups_state[chat_id] = "projects"
        group_ids = get_user_group_ids(chat_id)

        if not group_ids:
            await update.message.reply_text(
                "У тебя пока нет проектов.\n"
                "/search - Найти претендента на общий проект\n"
                "/requests - Посмотреть заявки"
            )
            return
        
        buttons = []

        for id in group_ids:
            group = get_group_by_id(id)
            if group:
                buttons.append([
                        InlineKeyboardButton(
                        text=group["name"],
                        callback_data=f"project_{id}"
                    )]
                )

        text = "Выбери проект:"
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(text, reply_markup=keyboard)
        return
    else:
        await update.message.reply_text(NOT_REGISTERED)

    response = MENU_RESPONSES.get(command, MENU_RESPONSES["unknown"])
    await update.message.reply_text(response)