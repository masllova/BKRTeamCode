from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import json
from datetime import datetime
from db.queries_groups import get_group_by_id, delete_group, update_group_name
from db.queries_users import get_user_group_ids, get_user_by_id, user_exists, get_user_role
from texts.menu import NOT_REGISTERED
from keyboards.menu import get_menu_keyboard

groups_state = {}

async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    group_ids = get_user_group_ids(chat_id)

    if user_exists(chat_id):
        groups_state[chat_id] = "projects"
        
        if not group_ids:
            await update.message.reply_text(
                "У Вас пока нет проектов.\n"
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
        text = "Выберите проект:"
        keyboard = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(text, reply_markup=keyboard)
        return
    else:
        await update.message.reply_text(NOT_REGISTERED)

async def handle_projects_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    state = groups_state.get(chat_id)

    if state.startswith("project_edit_name_"):
        project_id = int(state.split("_")[-1])
        update_group_name(project_id, text)
        await update.message.reply_text("Переименование прошло успешно!")
        project_text = get_text_for_project(project_id)

        keyboard = [
            [
                InlineKeyboardButton("Задачи", callback_data=f"project_tasks_{project_id}"),
                InlineKeyboardButton("Дедлайны", callback_data=f"project_deadlines_{project_id}")
            ],
            [
                InlineKeyboardButton("Файлы", callback_data=f"project_files_{project_id}"),
                InlineKeyboardButton("Настройки", callback_data=f"project_settings_{project_id}")
            ],
            [
                InlineKeyboardButton("Выйти в меню", callback_data="main_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if project_text:
            await update.message.reply_text(
            text=project_text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        else:
            await update.message.reply_text("Проект не найден или был удалён.")
            return
    else:
        return


async def handle_projects_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    print(data)

    if data.startswith("project_"):
        project_id = int(data.split("_")[-1])
        text = get_text_for_project(project_id)

        keyboard = [
            [
                InlineKeyboardButton("Задачи", callback_data=f"project_tasks_{project_id}"),
                InlineKeyboardButton("Дедлайны", callback_data=f"project_deadlines_{project_id}")
            ],
            [
                InlineKeyboardButton("Файлы", callback_data=f"project_files_{project_id}"),
                InlineKeyboardButton("Настройки", callback_data=f"project_settings_{project_id}")
            ],
            [
                InlineKeyboardButton("Выйти в меню", callback_data="main_menu")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if text:
            await query.message.reply_text(
            text=text,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
        else:
            await query.message.reply_text("Проект не найден или был удалён.")
            return
    elif data.startswith("project_settings_"):
        project_id, name = await extract_project_info(data, query)
        await query.message.reply_text(
            "Настройки проекта {name}",
            reply_markup= InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Изменить название", callback_data=f"project_edit_name_{project_id}")],
                    [InlineKeyboardButton("Удалить проект", callback_data=f"project_delete_{project_id}")]
                    [InlineKeyboardButton("Выйти в меню", callback_data=f"main_menu{project_id}")]
                ]
            )
        )
    elif data.startswith("project_files_"):
        return
    elif data.startswith("project_deadlines_"):
        return
    elif data.startswith("project_tasks_"):
        return
    elif data.startswith("project_delete_"):
        project_id, name = await extract_project_info(data, query)
        await query.message.reply_text(
            "Вы уверены что хотите удалить проект {name}?",
            reply_markup= InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Да", callback_data=f"project_confirmed_delete_{project_id}")],
                    [InlineKeyboardButton("Нет", callback_data=f"project_settings_{project_id}")]
                ]
            )
        )
    elif data.startswith("project_confirmed_delete_"):
        chat_id = update.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = "projects"
        delete_group(project_id)

        keyboard = get_menu_keyboard(get_user_role(chat_id))
        await query.message.reply_text(
            "Проект {name} был удален, можете продолжить работу в меню",
            reply_markup=keyboard
        )
    elif data.startswith("project_edit_name_"):
        chat_id = update.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = "project_edit_name_"
        await query.message.reply_text(
            "Ввдите новое название для проекта {name}"
        )
    elif data.startswith("main_menu"):
        return
    

    else:
        return
    
async def extract_project_info(data: str, query) -> tuple[int | None, str | None]:
    project_id = int(data.split("_")[-1])
    group = get_group_by_id(project_id)

    if not group:
        await query.message.reply_text("Проект не найден или был удалён.")
        return None, None

    name = group.get("name", "Без названия")
    return project_id, name

def get_text_for_project(project_id: int) -> str | None:
    group = get_group_by_id(project_id)

    if not group:
        return None

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

    return (
        f"<b>{name}</b>\n\n"
        f"Руководитель: {teacher_name}\n"
        f"Студент: {student_name}\n"
        f"Создан: "
        f"{created_at.strftime('%d.%m.%Y') if isinstance(created_at, datetime) else created_at}\n\n"
        f"📋 Актуальных задач: {task_count}\n"
        f"⏰ Актуальных дедлайнов: {deadline_count}"
    )