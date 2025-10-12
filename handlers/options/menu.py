from telegram import Update
from telegram.ext import ContextTypes
from keyboards.menu import BUTTON_TO_COMMAND

async def handle_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    command = BUTTON_TO_COMMAND.get(text)

    if command == "projects":
        await update.message.reply_text("📁 Открываю ваши проекты...")
    elif command == "requests":
        await update.message.reply_text("📨 Вот ваши заявки...")
    elif command == "search":
        await update.message.reply_text("🔍 Введите ключевые слова для поиска")
    elif command == "journal":
        await update.message.reply_text("📝 Ваш журнал активности")
    elif command == "stats":
        await update.message.reply_text("📊 Загружаю статистику...")
    elif command == "settings":
        await update.message.reply_text("⚙️ Открываю настройки")
    else:
        await update.message.reply_text("❓ Неизвестная команда.")