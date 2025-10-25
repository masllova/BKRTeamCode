from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu import BUTTON_TO_COMMAND, get_menu_keyboard
from db.queries_users import user_exists, get_user_role, get_user_group_ids
from db.queries_groups import get_group_by_id
from texts.menu import MENU_AVAILABLE, NOT_REGISTERED
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER
from handlers.options.search import search_state
from handlers.options.requests import requests_state
from handlers.options.projects import groups_state, groups_data_temp
from datetime import datetime, timedelta
import json

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
    groups_data_temp.pop(chat_id, None)

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
    elif command == "requests":
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
    elif command == "projects":
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
    elif command == "journal":
        group_ids = get_user_group_ids(chat_id)

        if not group_ids:
            await update.message.reply_text(
                "У тебя пока нет проектов по которым можно собрать журнал событий.\n"
                "/search - Найти претендента на общий проект\n"
                "/requests - Посмотреть заявки"
            )
            return
        text = "🗂️ Журнал задач и дедлайнов\n\n"

        for id in group_ids:
            group = get_group_by_id(id)

            if group:
                tasks = group.get("tasks") or {}

                if isinstance(tasks, str):
                    tasks = json.loads(tasks)
                if tasks:
                    text += f"\n📁 Проект: {group["name"]}"

                    for _, task in tasks.items():
                        if task.get("done"):
                            continue
                        text += f"\n- {task.get('name', '')}"
                deadlines = group.get("deadlines") or {}
                if isinstance(deadlines, str):
                    deadlines = json.loads(deadlines)

                today = datetime.today().date()
                limit_date = today + timedelta(days=28)

                # собираем дедлайны в пределах 28 дней
                upcoming = []
                for d in deadlines.values():
                    date_str = d.get("date", "")
                    text_str = d.get("text", "")
                    try:
                        deadline_date = datetime.strptime(date_str, "%d.%m.%Y").date()
                        if today <= deadline_date <= limit_date:
                            upcoming.append((deadline_date, text_str))
                    except ValueError:
                        continue

                if upcoming:
                    text += "\n\n📅  *Ближайшие дедлайны:*\n"
                    text += f"\n📁 {group['name']}"
                    for date, deadline_text in sorted(upcoming):
                        text += f"\n{date.strftime('%d.%m.%Y')} — {deadline_text}"
        role = get_user_role(chat_id)
        # ДЛЯ ТЕСТА
        keyboard = get_menu_keyboard("teacher") 

        await update.message.reply_text(text, reply_markup=keyboard)
        return
    elif command == "stats":
        return
    else:
        await update.message.reply_text(NOT_REGISTERED)
        return