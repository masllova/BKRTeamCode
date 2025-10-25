from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes
from io import BytesIO
import os
import json
from datetime import datetime
from db.queries_groups import (
    get_group_by_id, 
    delete_group, 
    update_group_name, 
    add_vkr_to_group,
    add_article_to_group,
    add_file_to_group,
    add_task_to_group,
    set_task_status
)
from texts.projects import (
    NO_PROJECTS, SELECT_PROJECT, RENAME_SUCCESS, PROJECT_NOT_FOUND, UPDATE_VKR_FILE_SUCCESS,
    UPDATE_VKR_LINK_SUCCESS, ADD_ARTICLE_FILE, ADD_ARTICLE_LINK, RESEND_LINK, SEND_LINK_OR_FILE,
    SEND_LINK_OR_FILE_WITH_ATTENTION, PROJECT_SETTINGS, SELECT_FILE_TYPE, CONFIRMED_DELETE_PROJECT,
    PROJECT_DELETED, ENTER_NEW_PROJECT_NAME, VKR_LINK, CURRENT_VKR_LINK, NOT_FOUND_VKR_FILE,
    NOT_FOUND_FILE, NOT_VKR_FILE, ARTICLES, SELECT_BUTTON_AFTER_WORK_WITH_FILES, NO_ARTICLES,
    END_OF_WORK, NO_NAME, NO_TEACHER, NO_STUDENT, ANOTHER_FILES, NO_ANOTHER_FILES, ADD_FILE,
    ADD_LINK, ADD_TASK_SUCCESS, ENTER_NEW_TASK, TASK, TASKS_LIST, NO_ACTUAL_TASKS, SELECT_ACTION,
    COMPLETE_TASK, COMPLETE_TASKS, ACTUAL_TASKS, NO_TASKS, NO_COMPLETE_TASKS, COMPLETE_TASK_LIST,
    ACTUAL_TASK, format_project
)
from keyboards.projects import (
    make_project_keyboard, make_back_keyboard, make_settings_keyboard, make_files_keyboard,
    make_add_keyboard, make_replace_keyboard, make_confirmed_delete_keyboard,
    make_complete_task_keyboard, make_complete_student_tasks_keyboard,
    make_teacher_tasks_empty_keyboard, make_teacher_tasks_keyboard,
    make_actual_student_tasks_keyboard, make_actual_task_keyboard
)
from db.queries_users import get_user_group_ids, get_user_by_id, user_exists, get_user_role
from db.queries_files import get_file
from texts.menu import NOT_REGISTERED
from keyboards.menu import get_menu_keyboard


groups_state = {}

async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    group_ids = get_user_group_ids(chat_id)

    if user_exists(chat_id):
        groups_state[chat_id] = "projects"
        
        if not group_ids:
            await update.message.reply_text(NO_PROJECTS)
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
        await update.message.reply_text(SELECT_PROJECT, reply_markup=InlineKeyboardMarkup(buttons))
        return
    else:
        await update.message.reply_text(NOT_REGISTERED)

async def handle_projects_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    state = groups_state.get(chat_id)

    if state.startswith("edit_name_"):
        text = update.message.text.strip()
        project_id = int(state.split("_")[-1])
        update_group_name(project_id, text)
        groups_state[chat_id] = "projects"

        await update.message.reply_text(RENAME_SUCCESS)
        project_text = get_text_for_project(project_id)

        if project_text:
            await update.message.reply_text(text=project_text, parse_mode="HTML", reply_markup=make_project_keyboard(project_id))
        else:
            await update.message.reply_text(PROJECT_NOT_FOUND)
            return
    if state.startswith("add_task_"):
        text = update.message.text.strip()
        project_id = int(state.split("_")[-1])
        add_task_to_group(project_id, text)
        groups_state[chat_id] = "projects"

        await update.message.reply_text(ADD_TASK_SUCCESS, reply_markup=make_back_keyboard("tasks", project_id))
    elif state.startswith("add_vkr_"):
        project_id = int(state.split("_")[-1])

        if update.message.document:
            # добавить ограничения 
            file = update.message.document
            file_name = file.file_name
            file_obj = await file.get_file()
            os.makedirs("files/vkr", exist_ok=True)
            save_path = os.path.join("files/vkr", file_name)
            base, ext = os.path.splitext(file_name)
            counter = 1

            while os.path.exists(save_path):
                save_path = os.path.join("files/vkr", f"{base}_{counter}{ext}")
                counter += 1
            await file_obj.download_to_drive(save_path)
            add_vkr_to_group(project_id, save_path, kind="file")
            groups_state[chat_id] = "projects"

            # кнопку заменить можно сюда тоже
            await update.message.reply_text(UPDATE_VKR_FILE_SUCCESS, reply_markup=make_back_keyboard("vkr", project_id))
        elif update.message.text:
            text = update.message.text.strip()

            if text.startswith("http://") or text.startswith("https://"):
                add_vkr_to_group(project_id, text, kind="link")
                groups_state[chat_id] = "projects"

                # кнопку замнить можно сюда тоже
                await update.message.reply_text(UPDATE_VKR_LINK_SUCCESS, reply_markup=make_back_keyboard("vkr", project_id))
            else:
                await update.message.reply_text(RESEND_LINK)
        else:
            await update.message.reply_text(SEND_LINK_OR_FILE)
    elif state.startswith("add_article_"):
        project_id = int(state.split("_")[-1])

        if update.message.document:
            file = update.message.document
            file_name = file.file_name
            file_obj = await file.get_file()
            os.makedirs("files/articles", exist_ok=True)
            save_path = os.path.join("files/articles", file_name)
            base, ext = os.path.splitext(file_name)
            counter = 1

            while os.path.exists(save_path):
                save_path = os.path.join("files/articles", f"{base}_{counter}{ext}")
                counter += 1

            await file_obj.download_to_drive(save_path)
            add_article_to_group(project_id, save_path, kind="file")
            groups_state[chat_id] = "projects"

            await update.message.reply_text(ADD_ARTICLE_FILE, reply_markup=make_back_keyboard("articles", project_id))
        elif update.message.text:
            text = update.message.text.strip()

            if text.startswith("http://") or text.startswith("https://"):
                add_article_to_group(project_id, text, kind="link")
                groups_state[chat_id] = "projects"

                await update.message.reply_text(ADD_ARTICLE_LINK, reply_markup=make_back_keyboard("articles", project_id))
            else:
                await update.message.reply_text(RESEND_LINK)
        else:
            await update.message.reply_text(SEND_LINK_OR_FILE)
    elif state.startswith("add_another_files_"):
        project_id = int(state.split("_")[-1])

        if update.message.document:
            file = update.message.document
            file_name = file.file_name
            file_obj = await file.get_file()
            os.makedirs("files/files", exist_ok=True)
            save_path = os.path.join("files/files", file_name)
            base, ext = os.path.splitext(file_name)
            counter = 1

            while os.path.exists(save_path):
                save_path = os.path.join("files/files", f"{base}_{counter}{ext}")
                counter += 1

            await file_obj.download_to_drive(save_path)
            add_file_to_group(project_id, save_path, kind="file")
            groups_state[chat_id] = "projects"

            await update.message.reply_text(ADD_FILE, reply_markup=make_back_keyboard("another_files_", project_id))
        elif update.message.text:
            text = update.message.text.strip()

            if text.startswith("http://") or text.startswith("https://"):
                add_file_to_group(project_id, text, kind="link")
                groups_state[chat_id] = "projects"

                await update.message.reply_text(ADD_LINK, reply_markup=make_back_keyboard("another_files_", project_id))
            else:
                await update.message.reply_text(RESEND_LINK)
        else:
            await update.message.reply_text(SEND_LINK_OR_FILE)
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

        if text:
            await query.message.reply_text(text=text, parse_mode="HTML", reply_markup=make_project_keyboard(project_id))
        else:
            await query.message.reply_text(PROJECT_NOT_FOUND)
            return
    elif data.startswith("settings_"):
        project_id, name = await extract_project_info(data, query)

        await query.message.reply_text(PROJECT_SETTINGS.format(name=name), reply_markup=make_settings_keyboard(project_id))
    elif data.startswith("files_"):
        project_id, name = await extract_project_info(data, query)

        await query.message.reply_text(SELECT_FILE_TYPE, reply_markup=make_files_keyboard(project_id))
    elif data.startswith("deadlines_"):
        return
    elif data.startswith("tasks_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        group = get_group_by_id(project_id)
        tasks = group.get("tasks") or {}

        if isinstance(tasks, str):
            tasks = json.loads(tasks)
        role = get_user_role(chat_id)

        if role == "student":
            if not tasks:
                await query.message.reply_text(NO_ACTUAL_TASKS, reply_markup=make_back_keyboard("project", project_id))
                return
            await query.message.reply_text(TASKS_LIST)
            for task_id, task in tasks.items():
                if task.get("done"):
                    continue
                await query.message.reply_text(
                    TASK.format(task=task.get('name', '')), 
                    reply_markup=make_complete_task_keyboard(task_id, project_id), 
                    parse_mode="Markdown"
                )
            await query.message.reply_text(SELECT_ACTION, reply_markup=make_complete_student_tasks_keyboard(project_id))
        else:
            if not tasks:
                await query.message.reply_text(NO_ACTUAL_TASKS, reply_markup=make_teacher_tasks_empty_keyboard(project_id))
                return
            active_lines = []
            done_lines = []

            for task_id, task in tasks.items():
                line = f"- {task.get('name', '')}"
                if task.get('done'):
                    done_lines.append(line)
                else:
                    active_lines.append(line)

            parts = []
            if active_lines:
                parts.append(ACTUAL_TASKS + "\n".join(active_lines))
            if done_lines:
                parts.append(COMPLETE_TASKS + "\n".join(done_lines))

            await query.message.reply_text(
                "\n\n".join(parts) if parts else NO_TASKS,
                reply_markup=make_teacher_tasks_keyboard(project_id),
                parse_mode="Markdown"
            )
    elif data.startswith("complete_"):
        parts = data.split("_")
        project_id = int(parts[-1])
        task_id = "_".join(parts[1:-1])
        set_task_status(project_id, task_id, True)

        await query.edit_message_text(text=COMPLETE_TASK)
    elif data.startswith("completed_tasks_"):
        project_id, name = await extract_project_info(data, query)
        group = get_group_by_id(project_id)
        tasks = group.get("tasks") or {}

        if not tasks:
            await query.message.reply_text(NO_COMPLETE_TASKS, reply_markup=make_back_keyboard("project", project_id))
            return
        await query.message.reply_text(COMPLETE_TASK_LIST)
        for task_id, task in tasks.items():
            if not task.get("done"):
                continue
            await query.message.reply_text(
                TASK.format(task=task.get('name', '')), 
                reply_markup=make_actual_task_keyboard(task_id, project_id), 
                parse_mode="Markdown"
            )
        await query.message.reply_text(SELECT_ACTION, reply_markup=make_actual_student_tasks_keyboard(project_id))
    elif data.startswith("actual_"):
        parts = data.split("_")
        project_id = int(parts[-1])
        task_id = "_".join(parts[1:-1])
        set_task_status(project_id, task_id, False)

        await query.edit_message_text(text=ACTUAL_TASK)
    elif data.startswith("delete_"):
        project_id, name = await extract_project_info(data, query)

        await query.message.reply_text(CONFIRMED_DELETE_PROJECT.format(name=name), reply_markup=make_confirmed_delete_keyboard(project_id))
    elif data.startswith("confirmed_delete_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        delete_group(project_id)

        await return_to_menu(update, context, PROJECT_DELETED)
    elif data.startswith("edit_name_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"edit_name_{project_id}"

        await query.message.reply_text(ENTER_NEW_PROJECT_NAME.format(name=name))
    elif data.startswith("add_task_"): 
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"add_task_{project_id}"

        await query.message.reply_text(ENTER_NEW_TASK)
    elif data.startswith("vkr_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        group = get_group_by_id(project_id)
        
        if not group:
            await query.message.reply_text(PROJECT_NOT_FOUND)
            return
        vkr_list = group.get("vkr", [])

        if vkr_list:
            vkr_item = vkr_list[0]

            if vkr_item["type"] == "link":
                await query.message.reply_text(
                    VKR_LINK.format(link=vkr_item['value']), 
                    reply_markup=make_replace_keyboard(project_id)
                )
            else:
                file_path = vkr_item["value"]
                file_bytes = get_file(file_path)

                if file_bytes:
                    await query.message.reply_text(CURRENT_VKR_LINK)
                    await context.bot.send_document(
                        chat_id=query.message.chat.id, 
                        document=InputFile(BytesIO(file_bytes), filename=os.path.basename(file_path)), 
                        reply_markup=make_replace_keyboard(project_id)
                    )
                else:
                    await query.message.reply_text(NOT_FOUND_VKR_FILE, reply_markup=make_back_keyboard("files", project_id))
        else:
            await query.message.reply_text(NOT_VKR_FILE, reply_markup=make_add_keyboard("vkr", project_id))
    elif data.startswith("add_vkr_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"add_vkr_{project_id}"
        await query.message.reply_text(SEND_LINK_OR_FILE_WITH_ATTENTION)
    elif data.startswith("articles_"):
        chat_id = query.message.chat.id
        project_id, name = await extract_project_info(data, query)
        group = get_group_by_id(project_id)

        if not group:
            await query.message.reply_text(PROJECT_NOT_FOUND)
            return
        articles_list = group.get("articles", [])

        if articles_list:
            links = []
            files = []

            for item in articles_list:
                if item["type"] == "link":
                    links.append(item["value"])
                elif item["type"] == "file":
                    files.append(item["value"])
            if links:
                links_text = ARTICLES + "\n".join([f"{idx+1}. {link}" for idx, link in enumerate(links)])
                
                await query.message.reply_text(links_text)
            if files:
                for file_path in files:
                    file_bytes = get_file(file_path)

                    if file_bytes:
                        await context.bot.send_document(
                            chat_id=query.message.chat.id,
                            document=InputFile(BytesIO(file_bytes), filename=os.path.basename(file_path))
                        )
                    else:
                        await query.message.reply_text(NOT_FOUND_FILE, reply_markup=make_back_keyboard("files", project_id))
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=SELECT_BUTTON_AFTER_WORK_WITH_FILES,
                reply_markup=make_add_keyboard("article", project_id)
            )
        else:
            await query.message.reply_text(NO_ARTICLES, reply_markup=make_add_keyboard("article", project_id))
    elif data.startswith("add_article_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"add_article_{project_id}"

        await query.message.reply_text(SEND_LINK_OR_FILE)
    elif data.startswith("another_files_"):
        chat_id = query.message.chat.id
        project_id, name = await extract_project_info(data, query)
        group = get_group_by_id(project_id)

        if not group:
            await query.message.reply_text(PROJECT_NOT_FOUND)
            return
        files_list = group.get("files", [])

        if files_list:
            links = []
            files = []

            for item in files_list:
                if item["type"] == "link":
                    links.append(item["value"])
                elif item["type"] == "file":
                    files.append(item["value"])
            if links:
                links_text = ANOTHER_FILES + "\n".join([f"{idx+1}. {link}" for idx, link in enumerate(links)])
                
                await query.message.reply_text(links_text)
            if files:
                for file_path in files:
                    file_bytes = get_file(file_path)

                    if file_bytes:
                        await context.bot.send_document(
                            chat_id=query.message.chat.id,
                            document=InputFile(BytesIO(file_bytes), filename=os.path.basename(file_path))
                        )
                    else:
                        await query.message.reply_text(NOT_FOUND_FILE, reply_markup=make_back_keyboard("files", project_id))
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text=SELECT_BUTTON_AFTER_WORK_WITH_FILES,
                reply_markup=make_add_keyboard("another_files", project_id)
            )
        else:
            await query.message.reply_text(NO_ANOTHER_FILES, reply_markup=make_add_keyboard("another_files", project_id))
    elif data.startswith("add_another_files_"):
        chat_id = query.message.chat_id
        project_id, name = await extract_project_info(data, query)
        groups_state[chat_id] = f"add_another_files_{project_id}"

        await query.message.reply_text(SEND_LINK_OR_FILE)
    elif data == "main_menu":
        await return_to_menu(update, context, END_OF_WORK)
        return
    else:
        return
    
async def extract_project_info(data: str, query) -> tuple[int | None, str | None]:
    project_id = int(data.split("_")[-1])
    group = get_group_by_id(project_id)

    if not group:
        await query.message.reply_text(PROJECT_NOT_FOUND)
        return None, None

    name = group.get("name", NO_NAME)
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

    name = group.get("name", NO_NAME)
    created_at = group.get("created_at", "")
    teacher_id = group.get("teacher_id")
    student_id = group.get("student_id")
    teacher = get_user_by_id(teacher_id) if teacher_id else None
    student = get_user_by_id(student_id) if student_id else None
    teacher_name = teacher["full_name"] if teacher else NO_TEACHER
    student_name = student["full_name"] if student else NO_STUDENT

    try:
        task_count = len(json.loads(group.get("tasks", "{}")))
    except Exception:
        task_count = 0

    try:
        deadline_count = len(json.loads(group.get("deadlines", "{}")))
    except Exception:
        deadline_count = 0

    return format_project(
        name=name,
        teacher_name=teacher_name,
        student_name=student_name,
        created_at=created_at,
        task_count=task_count,
        deadline_count=deadline_count
    )