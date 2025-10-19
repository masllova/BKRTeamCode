from telegram import Update
from telegram.ext import ContextTypes
from db.queries_requests import get_incoming_requests, get_outgoing_requests

requests_state = {}

async def handle_registration_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data

    if data == "incoming_requests":
        requests = get_incoming_requests(chat_id)
        if not requests:
            await query.message.reply_text("😔 У вас нет входящих заявок.")
            return

        text = "📩 Входящие заявки:\n\n"
        for r in requests:
            text += f"- Тема: {r['topic']}\n  От пользователя ID: {r['sender_id']}\n\n"

        await query.message.reply_text(text)
        return

    elif data == "outgoing_requests":
        requests = get_outgoing_requests(chat_id)
        if not requests:
            await query.message.reply_text("😔 У вас нет отправленных заявок.")
            return

        text = "📤 Отправленные заявки:\n\n"
        for r in requests:
            text += f"- Тема: {r['topic']}\n  Пользователю ID: {r['receiver_id']}\n\n"

        await query.message.reply_text(text)
        return