from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes
import os
import json
from datetime import datetime
from db.queries_groups import (
    get_group_by_id, 
    delete_group, 
    update_group_name, 
    add_vkr_to_group
)
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
                "У Вас пока нет проектов.\n\n"
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

    if state.startswith("edit_name_"):
        project_id = int(state.split("_")[-1])
        update_group_name(project_id, text)
        groups_state[chat_id] = "projects"
        await update.message.reply_text("Переименование прошло успешно!")
        project_text = get_text_for_project(project_id)

        keyboard = [
            [
                InlineKeyboardButton("Задачи", callback_data=f"tasks_{project_id}"),
                InlineKeyboardButton("Дедлайны", callback_data=f"deadlines_{project_id}")
            ],
            [
                InlineKeyboardButton("Файлы", callback_data=f"files_{project_id}"),
                InlineKeyboardButton("Настройки", callback_data=f"settings_{project_id}")
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
    elif state.startswith("add_vkr_"):
        project_id = int(state.split("_")[-1])

        # Если прислали файл
        if update.message.document:
            print("we have file")
            file = update.message.document
            file_name = file.file_name

            # Извлекаем сам файл
            file_obj = await file.get_file()
            os.makedirs("files/vkr", exist_ok=True)

            # Проверяем, не существует ли файл с таким именем
            save_path = os.path.join("files/vkr", file_name)
            base, ext = os.path.splitext(file_name)
            counter = 1
            while os.path.exists(save_path):
                save_path = os.path.join("files/vkr", f"{base}_{counter}{ext}")
                counter += 1

            await file_obj.download_to_drive(save_path)

            # Сохраняем в БД как новый ВКР
            add_vkr_to_group(project_id, save_path, kind="file")
            back_button= InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"vkr_{project_id}")]])
            groups_state[chat_id] = "projects"
            await update.message.reply_text(
                f"✅ Файл ВКР успешно обновлён: {os.path.basename(save_path)}",
                reply_markup=back_button
            )

        # Если прислали текст
        elif update.message.text:
            text = update.message.text.strip()

            # Простейшая валидация ссылки
            if text.startswith("http://") or text.startswith("https://"):
                add_vkr_to_group(project_id, text, kind="link")
                groups_state[chat_id] = "projects"
                back_button= InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"vkr_{project_id}")]])
                await update.message.reply_text("✅ Ссылка на ВКР успешно обновлена.", reply_markup=back_button)
            else:
                await update.message.reply_text(
                    "Похоже, вы отправили не ссылку. Пожалуйста, пришлите корректную ссылку, начинающуюся с http:// или https:// \n или пришлите файл"
                )

        else:
            await update.message.reply_text("⚠️ Пожалуйста, пришлите файл или ссылку для добавления ВКР.")
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
                InlineKeyboardButton("Задачи", callback_data=f"tasks_{project_id}"),
                InlineKeyboardButton("Дедлайны", callback_data=f"deadlines_{project_id}")
            ],
            [
                InlineKeyboardButton("Файлы", callback_data=f"files_{project_id}"),
                InlineKeyboardButton("Настройки", callback_data=f"settings_{project_id}")
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
    elif data.startswith("settings_"):
        project_id, name = await extract_project_info(data, query)
        await query.message.reply_text(
            f"Настройки проекта {name}",
            reply_markup= InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Изменить название", callback_data=f"edit_name_{project_id}")],
                    [InlineKeyboardButton("Удалить проект", callback_data=f"delete_{project_id}")],
                    [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
                ]
            )
        )
    elif data.startswith("files_"):
        project_id, name = await extract_project_info(data, query)
        await query.message.reply_text(
            "Выберите тип файлов:",
            reply_markup= InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Статьи", callback_data=f"articles_{project_id}")],
                    [InlineKeyboardButton("Файл ВКР", callback_data=f"vkr_{project_id}")],
                    [InlineKeyboardButton("Прочие файлы", callback_data=f"files_{project_id}")],
                    [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
                ]
            )
        )
    elif data.startswith("deadlines_"):
        return
    elif data.startswith("tasks_"):
        return
    elif data.startswith("delete_"):
        project_id, name = await extract_project_info(data, query)
        await query.message.reply_text(
            f"Вы уверены что хотите удалить проект {name}?",
            reply_markup= InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Да", callback_data=f"confirmed_delete_{project_id}")],
                    [InlineKeyboardButton("Нет", callback_data=f"settings_{project_id}")]
                ]
            )
        )
    elif data.startswith("confirmed_delete_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        delete_group(project_id)
        await return_to_menu(update, context, "Проект был удален, можете продолжить работу в меню")
        return
    elif data.startswith("edit_name_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"edit_name_{project_id}"
        await query.message.reply_text(
            f"Введите новое название для проекта {name}"
        )
    elif data.startswith("vkr_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)

        group = get_group_by_id(project_id)
        if not group:
            await query.message.reply_text("❌ Проект не найден или был удалён.")
            return

        vkr_list = group.get("vkr", [])
        add_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Добавить", callback_data=f"add_vkr_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"files_{project_id}")]
        ])

        replace_buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Заменить", callback_data=f"add_vkr_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"files_{project_id}")]
        ])

        if vkr_list:
            vkr_item = vkr_list[0]

            if vkr_item["type"] == "link":
                text = f"📎 Ссылка на ВКР:\n{vkr_item['value']}"
                await query.message.reply_text(text, reply_markup=replace_buttons)
            else:
                file_path = vkr_item["value"]
                if os.path.exists(file_path):
                    await query.message.reply_text("📄 Ваш текущий файл ВКР:")
                    await context.bot.send_document(
                        chat_id=query.message.chat.id,
                        document=InputFile(file_path, filename=os.path.basename(file_path)),
                        reply_markup=replace_buttons
                    )
                else:
                    await query.message.reply_text(
                        "⚠️ Файл ВКР не найден.",
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"files_{project_id}")]])
                    )
        else:
            await query.message.reply_text(
                "Файл ВКР отсутствует",
                reply_markup=add_buttons
            )
    elif data.startswith("add_vkr_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"add_vkr_{project_id}"
        await query.message.reply_text("Добавьте файл или пришлите ссылку.\nОбратите внимание, что это заменит прошлый файл без возможности вернуть его. Если нужно сохранить старый файл — лучше перейдите в раздел прочие файлы.")

    elif data.startswith("articles_"):
        await return_to_menu(update, context, "Работа с проектом завершена")
        return
    # elif data.startswith("project_"):
    #     await return_to_menu(update, context, "Работа с проектом завершена")
    #     return
    elif data == "main_menu":
        await return_to_menu(update, context, "Работа с проектом завершена")
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

async def return_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    query = update.callback_query
    chat_id = query.message.chat_id
    role = get_user_role(chat_id)
    keyboard = get_menu_keyboard(role)
    await query.message.reply_text(text, reply_markup=keyboard)
    groups_state.pop(chat_id, None)
    return

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