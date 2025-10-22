from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.queries_requests import get_incoming_requests, get_outgoing_requests, respond_request, get_request_users
from db.queries_users import get_user_by_id, user_exists
from texts.menu import NOT_REGISTERED
from texts.requests import (
    NO_INCOMING_REQUESTS,
    NO_OUTGOING_REQUESTS, 
    REQUEST_ACCEPTED_TEXT_RECEIVER, 
    REQUEST_ACCEPTED_TEXT_SENDER, 
    REQUEST_DECLINED_TEXT_RECEIVER, 
    REQUEST_DECLINED_TEXT_SENDER, 
    REQUEST_DELETED_TEXT, 
    REQUEST_REMINDER_SENT_TEXT, 
    REQUEST_REMINDER_RECEIVED_TEXT, 
    INCOMING_REQUEST_TEMPLATE, 
    OUTGOING_REQUEST_TEMPLATE
)
from keyboards.requests import ACCEPT_BUTTON, DECLINE_BUTTON, DELETE_BUTTON, REMIND_BUTTON

requests_state = {}

async def view_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        requests_state[chat_id] = "awaiting_type"

        requests = get_incoming_requests(chat_id)

        if not requests:
            await update.message.reply_text(NO_INCOMING_REQUESTS)
            # тут расширение ввода профиля
            return
        for r in requests:
            await update.message.reply_text(
                INCOMING_REQUEST_TEMPLATE.format(topic=r['topic'], sender=r['sender_name']), 
                reply_markup=InlineKeyboardMarkup([[ACCEPT_BUTTON, DECLINE_BUTTON]])
            )
        return
    else:
        await update.message.reply_text(NOT_REGISTERED)

async def handle_requests_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data

    if data == "incoming_requests":
        requests = get_incoming_requests(chat_id)

        if not requests:
            await query.message.reply_text(NO_INCOMING_REQUESTS)
            # тут расширение ввода профиля
            return
        for r in requests:
            await query.message.reply_text(
                INCOMING_REQUEST_TEMPLATE.format(topic=r['topic'], sender=r['sender_name']), 
                reply_markup=InlineKeyboardMarkup([[ACCEPT_BUTTON, DECLINE_BUTTON]])
            )
        return

    elif data == "outgoing_requests":
        requests = get_outgoing_requests(chat_id)

        if not requests:
            await query.message.reply_text(NO_OUTGOING_REQUESTS)
            # тут расширение ввода профиля
            return
        for r in requests:
            await query.message.reply_text(
                OUTGOING_REQUEST_TEMPLATE.format(topic=r['topic'],receiver=r['receiver_name']), 
                reply_markup=InlineKeyboardMarkup([[DELETE_BUTTON, REMIND_BUTTON]])
            )
        return
    elif data.startswith("accept_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        respond_request(request_id)

        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=REQUEST_ACCEPTED_TEXT_RECEIVER
        )
        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text=REQUEST_ACCEPTED_TEXT_SENDER.format(sender_name=sender_info['full_name'])
        )
    elif data.startswith("decline_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        respond_request(request_id)

        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=REQUEST_DECLINED_TEXT_RECEIVER
        )
        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text=REQUEST_DECLINED_TEXT_SENDER.format(receiver_name=sender_info['full_name'])
        )
    elif data.startswith("delete_request_"):
        request_id = int(data.split("_")[-1])
        respond_request(request_id)
        await query.message.reply_text(REQUEST_DELETED_TEXT)

    elif data.startswith("remind_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text=REQUEST_REMINDER_SENT_TEXT
        )
        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=REQUEST_REMINDER_RECEIVED_TEXT.format(sender_name=sender_info['full_name'])
        )