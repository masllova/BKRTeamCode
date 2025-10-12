from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.options.start import start
from handlers.options.registration import handle_text
from handlers.handle_callback import handle_callback
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()