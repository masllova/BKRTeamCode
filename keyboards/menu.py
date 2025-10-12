from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STUDENT_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📚 Проекты", callback_data="projects"),
        InlineKeyboardButton("📨 Заявки", callback_data="requests"),
    ],
    [
        InlineKeyboardButton("🔍 Поиск", callback_data="search"),
        InlineKeyboardButton("📝 Журнал", callback_data="journal"),
    ],
    [
        InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
    ],
])

TEACHER_MENU = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("📚 Проекты", callback_data="projects"),
        InlineKeyboardButton("📊 Статистика", callback_data="stats"),
    ],
    [
        InlineKeyboardButton("🔍 Поиск", callback_data="search"),
        InlineKeyboardButton("⚙️ Настройки", callback_data="settings"),
    ],
])