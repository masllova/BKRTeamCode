from telegram import Update
from telegram.ext import ContextTypes
from handlers.registration import user_state

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    user_state[chat_id] = "awaiting_name"

    await update.message.reply_text("Привет! Я VKRTeamBot. Введи своё ФИО:")