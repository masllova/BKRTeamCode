from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.options.start import start
from handlers.options.menu import menu
from handlers.options.requests import view_requests
from handlers.options.search import search
from handlers.options.projects import projects
from handlers.options.settings import profile
from handlers.handle_text import handle_text
from handlers.handle_callback import handle_callback
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("view_requests", view_requests))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("projects", projects))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(MessageHandler((filters.TEXT | filters.Document.ALL) & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()