from telegram import Update
from telegram.ext import ContextTypes

async def handle_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    command = query.data

    if command == "projects":
        await query.message.reply_text("📁 Открываю ваши проекты...")
    elif command == "requests":
        await query.message.reply_text("📨 Вот ваши заявки...")
    elif command == "search":
        await query.message.reply_text("🔍 Введите ключевые слова для поиска")
    elif command == "journal":
        await query.message.reply_text("📝 Ваш журнал активности")
    elif command == "stats":
        await query.message.reply_text("📊 Загружаю статистику...")
    elif command == "settings":
        await query.message.reply_text("⚙️ Открываю настройки")
    else:
        await query.message.reply_text("❓ Неизвестная команда.")