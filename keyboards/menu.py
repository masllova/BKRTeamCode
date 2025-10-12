from telegram import ReplyKeyboardMarkup

STUDENT_MENU_BUTTONS = [
    ["📚 Открыть проекты", "📨 Мои заявки"],
    ["🔍 Поиск", "📝 Журнал"],
    ["⚙️ Настройки"]
]

TEACHER_MENU_BUTTONS = [
    ["📚 Открыть проекты", "📊 Статистика"],
    ["🔍 Поиск", "⚙️ Настройки"]
]

BUTTON_TO_COMMAND = {
    "📚 Открыть проекты": "projects",
    "📨 Мои заявки": "requests",
    "🔍 Поиск": "search",
    "📝 Журнал": "journal",
    "⚙️ Настройки": "settings",
    "📊 Статистика": "stats",
}

def get_menu_keyboard(role: str) -> ReplyKeyboardMarkup:
    buttons = STUDENT_MENU_BUTTONS if role == "student" else TEACHER_MENU_BUTTONS
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=False)