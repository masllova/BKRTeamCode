from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.start import start
from handlers.registration import handle_name_callback, handle_university_callback, handle_role_callback, handle_stage_callback
from config import TOKEN

def state_is(expected_state):
    async def _filter(_, update):
        chat_id = update.message.chat_id
        return user_state.get(chat_id) == expected_state
    return filters.Create(_filter)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & ~state_is("awaiting_university"), handle_name_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & state_is("awaiting_university"), handle_university_callback))

    app.add_handler(CallbackQueryHandler(handle_role_callback))
    app.add_handler(CallbackQueryHandler(handle_stage_callback))

    print("🚀 Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()