from telegram import ReplyKeyboardMarkup

STUDENT_MENU_BUTTONS = [
    "📚 Проекты",
    "📝 Журнал",
    "📨 Заявки",
    "🔍 Поиск", 
    "⚙️ Настройки"
]

TEACHER_MENU_BUTTONS = [
    "📚 Проекты", 
    "📊 Статистика",
    "📨 Заявки",
    "🔍 Поиск", 
    "⚙️ Настройки"
]

BUTTON_TO_COMMAND = {
    "📚 Проекты": "projects",
    "📝 Журнал": "journal",
    "📊 Статистика": "stats",
    "📨 Заявки": "requests",
    "🔍 Поиск": "search",
    "⚙️ Настройки": "settings",
}

def get_menu_keyboard(role: str) -> ReplyKeyboardMarkup:
    buttons = STUDENT_MENU_BUTTONS if role == "student" else TEACHER_MENU_BUTTONS
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)