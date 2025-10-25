from datetime import datetime
from typing import Union

NO_PROJECTS = "У Вас пока нет проектов.\n\n/search - Найти претендента на общий проект\n/requests - Посмотреть заявки"
SELECT_PROJECT = "Выберите проект:"
RENAME_SUCCESS = "Переименование прошло успешно!"
ADD_TASK_SUCCESS = "Добавление задачи прошло успешно!"
PROJECT_NOT_FOUND = "Проект не найден или был удалён."
UPDATE_VKR_FILE_SUCCESS = "✅ Файл ВКР успешно обновлён"
UPDATE_VKR_LINK_SUCCESS = "✅ Ссылка на ВКР успешно обновлена."
ADD_ARTICLE_FILE = "✅ Файл статьи успешно добавлен"
ADD_ARTICLE_LINK = "✅ Ссылка на статью успешно добавлена."
ADD_FILE = "✅ Файл успешно добавлен"
ADD_LINK = "✅ Ссылка успешно добавлена."
RESEND_LINK = "Похоже, вы отправили не ссылку. Пожалуйста, пришлите корректную ссылку, начинающуюся с http:// или https:// \n или пришлите файл"
SEND_LINK_OR_FILE = "Пожалуйста, пришлите файл или ссылку"
SEND_LINK_OR_FILE_WITH_ATTENTION = "Добавьте файл или пришлите ссылку.\nОбратите внимание, что это заменит прошлый файл без возможности вернуть его. Если нужно сохранить старый файл — лучше перейдите в раздел прочие файлы."
PROJECT_SETTINGS = "Настройки проекта {name}"
SELECT_FILE_TYPE = "Выберите тип файлов:"
CONFIRMED_DELETE_PROJECT = "Вы уверены что хотите удалить проект {name}?"
PROJECT_DELETED = "Проект был удален, можете продолжить работу в меню"
ENTER_NEW_PROJECT_NAME = "Введите новое название для проекта {name}"
ENTER_NEW_TASK = "Введите текст задачи"
VKR_LINK = "📎 Ссылка на ВКР:\n{link}"
CURRENT_VKR_LINK = "📄 Ваш текущий файл ВКР:"
NOT_FOUND_VKR_FILE = "⚠️ Файл ВКР не найден."
NOT_FOUND_FILE = "⚠️ Файл не найден"
NOT_VKR_FILE = "Файл ВКР отсутствует"
ARTICLES = "📎 Статьи:\n"
ANOTHER_FILES = "📎 Прочие файлы:\n"
SELECT_BUTTON_AFTER_WORK_WITH_FILES = "Выберите действие после того, как закончите работу с файлами"
NO_ARTICLES = "Статей пока нет."
NO_ANOTHER_FILES = "Прочих файлов пока нет."
END_OF_WORK = "Работа с проектом завершена"
NO_NAME = "Без названия"
NO_TEACHER = "Неизвестный руководитель"
NO_STUDENT = "Неизвестный студент"
NO_ACTUAL_TASKS = "Нет активных задач."
NO_COMPLETE_TASKS = "Нет выполненых задач."
NO_TASKS = "Нет задач"
TASKS_LIST = "Список актуальных задач"
COMPLETE_TASK_LIST = "Список выполненых задач"
TASK = "*Задача:* {task}"
SELECT_ACTION = "Выберите действие:"
COMPLETE_TASK = "Задача выполнена"
ACTUAL_TASK = "Задача в работе"
COMPLETE_TASKS = "Выполненные задачи:\n"
ACTUAL_TASKS = "Актуальные задачи:\n"
ENTER_COMMENT = "Напишите комментарий для {name}\nСтудет увидет его в уведомлении"
REMIND = "🔔 {teacher_name} напоминает о задачах в проекте {project_name}\n\nКомментарий: {comment}\nНе забудьте проверить список активных задач и отметить выполненные, когда завершите.\nМожете увидеть совместный проект в разделе /projects."
REMIND_SUCCSESS = "✅ Уведомление отправлено!"
DEADLINE_LIST = "Дедлайны по проекту:"
NO_DEADLINE = "Пока дедлайнов нет."

def format_project(
    name: str,
    teacher_name: str,
    student_name: str,
    created_at: Union[datetime, str],
    task_count: int,
    deadline_count: int
) -> str:
    return (
        f"<b>{name}</b>\n\n"
        f"Руководитель: {teacher_name}\n"
        f"Студент: {student_name}\n"
        f"Создан: "
        f"{created_at.strftime('%d.%m.%Y') if isinstance(created_at, datetime) else created_at}\n\n"
        f"📋 Актуальных задач: {task_count}\n"
        f"⏰ Актуальных дедлайнов: {deadline_count}"
    )