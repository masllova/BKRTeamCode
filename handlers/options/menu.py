from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.menu import BUTTON_TO_COMMAND, get_menu_keyboard
from keyboards.settings import SELECT_SETTINGS_KEYBOARD
from db.queries_users import user_exists, get_user_role, get_user_group_ids, get_user_by_id
from db.queries_groups import get_group_by_id
from texts.menu import MENU_AVAILABLE, NOT_REGISTERED, NO_STUDENT
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER
from handlers.options.search import search_state
from handlers.options.requests import requests_state
from handlers.options.projects import groups_state, groups_data_temp
from handlers.options.settings import settings_state
from datetime import datetime, timedelta
from telegram.helpers import escape_markdown
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
    settings_state.pop(chat_id, None)

    print(command)

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
    elif command == "settings":
        settings_state[chat_id] = "settings"
        await update.message.reply_text("Выберите раздел настроек", reply_markup=SELECT_SETTINGS_KEYBOARD)
    elif command == "journal":
        group_ids = get_user_group_ids(chat_id)

        if not group_ids:
            await update.message.reply_text(
                "У Вас пока нет проектов по которым можно собрать журнал событий.\n"
                "/search - Найти претендента на общий проект\n"
                "/requests - Посмотреть заявки"
            )
            return
        text = "🗂️ Журнал задач и дедлайнов\n\n📁 *Проекты:*"

        print(text)

        for id in group_ids:
            group = get_group_by_id(id)

            if group:
                tasks = group.get("tasks") or {}

                if isinstance(tasks, str):
                    tasks = json.loads(tasks)
                if tasks:
                    text += f"\nПроект: {group["name"]}"
                    print(text)

                    for _, task in tasks.items():
                        if task.get("done"):
                            continue
                        text += f"\n- {task.get('name', '')}"
                        print(text)
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
                    text += "\n\n📅  *Ближайшие дедлайны (на 28 дней):*\n"
                    print(text)
                    text += f"\nПроект: {group['name']}"
                    print(text)
                    for date, deadline_text in sorted(upcoming):
                        text += f"\n{date.strftime('%d.%m.%Y')} — {deadline_text}"
                        print(text)
        role = get_user_role(chat_id)
        keyboard = get_menu_keyboard(role) 

        await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
        return
    elif command == "stats":
        group_ids = get_user_group_ids(chat_id)

        if not group_ids:
            await update.message.reply_text(
                "У Вас пока нет проектов по которым можно собрать статистику.\n"
                "/search - Найти претендента на общий проект\n"
                "/requests - Посмотреть заявки"
            )
            return

        role = get_user_role(chat_id)
        keyboard = get_menu_keyboard(role)

        await update.message.reply_text("📊 Статистика", reply_markup=keyboard)

        for id in group_ids:
            group = get_group_by_id(id)
            if not group:
                continue

            # Сохраняем все блоки текста в список
            blocks = []

            # 1. Проект
            project_name_safe = escape_markdown(group['name'], version=2)
            blocks.append(f"*Проект*: {project_name_safe}")

            # 2. Файлы и статьи
            files_text = "📎 Файлы:\n"
            vkr_list = group.get("vkr", [])
            files_list = group.get("files", [])
            articles_list = group.get("articles", [])

            files_text += "Файл ВКР прикреплен" if vkr_list else "Файл ВКР отсутствует"
            files_text += f"\nКол-во прочих файлов: {len(files_list)}"
            files_text += f"\nКол-во статей: {len(articles_list)}"
            blocks.append(escape_markdown(files_text, version=2))

            # 3. Задачи
            tasks = group.get("tasks") or {}
            if isinstance(tasks, str):
                tasks = json.loads(tasks)
            if tasks:
                tasks_text = "📌 Задачи:\n"
                tasks_text += f"- Всего: {len(tasks)}\n"
                tasks_text += f"- Выполнено: {sum(1 for task in tasks.values() if task.get('done', False))}"
                blocks.append(escape_markdown(tasks_text, version=2))

            # 4. Дедлайны
            deadlines = group.get("deadlines") or {}
            if isinstance(deadlines, str):
                deadlines = json.loads(deadlines)

            today = datetime.today().date()
            limit_date = today + timedelta(days=28)
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
                deadlines_text = "📅 Ближайшие дедлайны (на 28 дней):\n"
                for date, deadline_text in sorted(upcoming):
                    deadlines_text += f"{date.strftime('%d.%m.%Y')} — {escape_markdown(deadline_text, version=2)}\n"
                blocks.append(deadlines_text.strip())

            # 5. Студент
            student_id = group.get("student_id")
            student = get_user_by_id(student_id) if student_id else None
            student_name = escape_markdown(student["full_name"], version=2) if student else NO_STUDENT
            student_email = escape_markdown(student["email"], version=2) if student and student.get("email") else "-"
            blocks.append(f"👤 Студент: {student_name}\nПочта: {student_email}")

            # Отправка всех блоков отдельно
            for block in blocks:
                await update.message.reply_text(block, reply_markup=keyboard, parse_mode="MarkdownV2")
    else:
        await update.message.reply_text(NOT_REGISTERED)
        return