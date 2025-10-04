from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.start import start
from handlers.registration import handle_message
from config import TOKEN

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()