from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_requests import (
    get_incoming_requests, get_outgoing_requests, respond_request, 
    get_request_users, get_request_topic
)
from db.queries_users import (
    get_user_by_id, user_exists, add_group_to_user, 
    is_profile_complete_by_id, get_notifications_state
)
from db.queries_groups import create_group
from texts.menu import NOT_REGISTERED
from texts.requests import (
    NO_INCOMING_REQUESTS, NO_OUTGOING_REQUESTS, REQUEST_ACCEPTED_TEXT_RECEIVER, 
    REQUEST_ACCEPTED_TEXT_SENDER, REQUEST_DECLINED_TEXT_RECEIVER, REQUEST_DECLINED_TEXT_SENDER, 
    REQUEST_DELETED_TEXT, REQUEST_REMINDER_SENT_TEXT, REQUEST_REMINDER_RECEIVED_TEXT, 
    INCOMING_REQUEST_TEMPLATE, OUTGOING_REQUEST_TEMPLATE, NO_INCOMING_REQUESTS_WITH_RECOMENDATION
)
from keyboards.requests import build_incoming_keyboard, build_outgoing_keyboard

requests_state = {}

async def view_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id

    if user_exists(chat_id):
        requests_state[chat_id] = "awaiting_type"

        requests = get_incoming_requests(chat_id)

        if not requests:
            is_complete = is_profile_complete_by_id(chat_id)

            if is_complete:
                await update.message.reply_text(NO_INCOMING_REQUESTS)
            else:
                await update.message.reply_text(NO_INCOMING_REQUESTS_WITH_RECOMENDATION)
            return
        for r in requests:
            await update.message.reply_text(
                INCOMING_REQUEST_TEMPLATE.format(topic=r['topic'], sender=r['sender_name']), 
                reply_markup=InlineKeyboardMarkup(build_incoming_keyboard(r['id']))
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
            is_complete = is_profile_complete_by_id(chat_id)

            if is_complete:
                await query.message.reply_text(NO_INCOMING_REQUESTS)
            else:
                await query.message.reply_text(NO_INCOMING_REQUESTS_WITH_RECOMENDATION)
            return
        for r in requests:
            await query.message.reply_text(
                INCOMING_REQUEST_TEMPLATE.format(topic=r['topic'], sender=r['sender_name']), 
                reply_markup=InlineKeyboardMarkup(build_incoming_keyboard(r['id']))
            )
        return

    elif data == "outgoing_requests":
        requests = get_outgoing_requests(chat_id)

        if not requests:
            await query.message.reply_text(NO_OUTGOING_REQUESTS)
            return
        for r in requests:
            await query.message.reply_text(
                OUTGOING_REQUEST_TEMPLATE.format(topic=r['topic'],receiver=r['receiver_name']), 
                reply_markup=InlineKeyboardMarkup(build_outgoing_keyboard(r['id']))
            )
        return
    elif data.startswith("accept_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        if sender_info["role"] == "teacher":
            teacher_id = sender_id
            student_id = receiver_id
        else:
            teacher_id = receiver_id
            student_id = sender_id

        group_name = get_request_topic(request_id)
        group_id = create_group(teacher_id, student_id, group_name)
        add_group_to_user(teacher_id, group_id)
        add_group_to_user(student_id, group_id)
        respond_request(request_id)

        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=REQUEST_ACCEPTED_TEXT_RECEIVER
        )
        enabled = get_notifications_state(sender_info["telegram_id"])
        
        if enabled:
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
        enabled = get_notifications_state(sender_info["telegram_id"])

        if enabled:
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
        enabled = get_notifications_state(sender_info["telegram_id"])

        if enabled:
            await context.bot.send_message(
                chat_id=receiver_info["telegram_id"],
                text=REQUEST_REMINDER_RECEIVED_TEXT.format(sender_name=sender_info['full_name'])
            )