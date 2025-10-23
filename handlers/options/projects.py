from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import json
from datetime import datetime
from db.queries_groups import get_group_by_id
from db.queries_users import get_user_group_ids, get_user_by_id, user_exists
from texts.menu import NOT_REGISTERED

groups_state = {}

async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    group_ids = get_user_group_ids(chat_id)

    if user_exists(chat_id):
        groups_state[chat_id] = "select_project"
        
        if not group_ids:
            await update.message.reply_text(
                "У тебя пока нет проектов.\n"
                "/search - Найти претендента на общий проект\n"
                "/requests - Посмотреть заявки"
            )
            return

        buttons = []

        for id in group_ids:
            print('id from group_ids')
            print(id)
            group = get_group_by_id(id)
            print('group_id')
            print(group['id'])
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

async def handle_projects_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

async def handle_projects_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    print(data)

    if data.startswith("project_"):
        project_id = int(data.split("_")[-1])
        group = get_group_by_id(project_id)

        if not group:
            await query.edit_message_text("❌ Проект не найден или был удалён.")
            return

        name = group.get("name", "Без названия")
        created_at = group.get("created_at", "")
        teacher_id = group.get("teacher_id")
        student_id = group.get("student_id")

        teacher = get_user_by_id(teacher_id) if teacher_id else None
        student = get_user_by_id(student_id) if student_id else None

        teacher_name = teacher["full_name"] if teacher else "Неизвестный руководитель"
        student_name = student["full_name"] if student else "Неизвестный студент"

        try:
            task_count = len(json.loads(group.get("tasks", "{}")))
        except Exception:
            task_count = 0

        try:
            deadline_count = len(json.loads(group.get("deadlines", "{}")))
        except Exception:
            deadline_count = 0

        text = (
            f"📘 <b>{name}</b>\n"
            f"👨‍🏫 Руководитель: {teacher_name}\n"
            f"🎓 Студент: {student_name}\n"
            f"🗓 Создан: "
            f"{created_at.strftime('%d.%m.%Y') if isinstance(created_at, datetime) else created_at}\n\n"
            f"📋 Задач: {task_count}\n"
            f"⏰ Дедлайнов: {deadline_count}"
        )

        keyboard = [
            [
                InlineKeyboardButton("📂 Файлы", callback_data=f"project_files_{project_id}"),
                InlineKeyboardButton("⚙️ Настройки", callback_data=f"project_settings_{project_id}")
            ],
            [
                InlineKeyboardButton("🧾 Задачи", callback_data=f"project_tasks_{project_id}"),
                InlineKeyboardButton("📅 Дедлайны", callback_data=f"project_deadlines_{project_id}")
            ],
            [
                InlineKeyboardButton("⬅️ В меню", callback_data="main_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    else:
        return