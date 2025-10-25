from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def make_project_keyboard(project_id):
    return InlineKeyboardMarkup(
        [
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
    )

def make_back_keyboard(command, project_id):
    return InlineKeyboardMarkup([[InlineKeyboardButton("Назад", callback_data=f"{command}_{project_id}")]])

def make_settings_keyboard(project_id):
    return InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Изменить название", callback_data=f"edit_name_{project_id}")],
                    [InlineKeyboardButton("Удалить проект", callback_data=f"delete_{project_id}")],
                    [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
                ]
            )

def make_files_keyboard(project_id):
    return InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Статьи", callback_data=f"articles_{project_id}")],
                    [InlineKeyboardButton("Файл ВКР", callback_data=f"vkr_{project_id}")],
                    [InlineKeyboardButton("Прочие файлы", callback_data=f"another_files_{project_id}")],
                    [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
                ]
            )

def make_confirmed_delete_keyboard(project_id):
    return InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Да", callback_data=f"confirmed_delete_{project_id}")],
                    [InlineKeyboardButton("Нет", callback_data=f"settings_{project_id}")]
                ]
            )

def make_add_keyboard(file_type, project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Добавить", callback_data=f"add_{file_type}_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"files_{project_id}")]
        ])

def make_replace_keyboard(project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Заменить", callback_data=f"add_vkr_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"files_{project_id}")]
        ])

def make_complete_task_keyboard(task_id, project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Выполнено", callback_data=f"complete_{task_id}_{project_id}")]
        ])

def make_actual_task_keyboard(task_id, project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("В работе", callback_data=f"actual_{task_id}_{project_id}")]
        ])

def make_complete_student_tasks_keyboard(project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Показать выполненные задачи", callback_data=f"completed_tasks_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
        ])

def make_actual_student_tasks_keyboard(project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Показать актуальные задачи", callback_data=f"completed_tasks_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
        ])

def make_teacher_tasks_empty_keyboard(project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Добавить задачу", callback_data=f"add_task_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
        ])

def make_teacher_tasks_keyboard(project_id):
    return InlineKeyboardMarkup([
            [InlineKeyboardButton("Добавить задачу", callback_data=f"add_task_{project_id}")],
            [InlineKeyboardButton("Напомнить студенту о задачах", callback_data=f"remind_{project_id}")],
            [InlineKeyboardButton("Назад", callback_data=f"project_{project_id}")]
        ])