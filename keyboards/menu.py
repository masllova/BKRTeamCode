from telegram import KeyboardButton, ReplyKeyboardMarkup

STUDENT_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("🎓 Проекты"), KeyboardButton("📨 Заявки")],
    [KeyboardButton("🔍 Поиск"), KeyboardButton("📘 Журнал")],
    [KeyboardButton("⚙️ Настройки")]
], resize_keyboard=True)

TEACHER_MENU = ReplyKeyboardMarkup([
    [KeyboardButton("📊 Статистика"), KeyboardButton("🎓 Проекты")],
    [KeyboardButton("📨 Заявки"), KeyboardButton("🔍 Поиск")],
    [KeyboardButton("⚙️ Настройки")]
], resize_keyboard=True)