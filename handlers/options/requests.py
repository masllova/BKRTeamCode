from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.queries_requests import get_incoming_requests, get_outgoing_requests, respond_request, get_request_users
from db.queries_users import get_user_by_id

requests_state = {}

async def handle_requests_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data

    if data == "incoming_requests":
        requests = get_incoming_requests(chat_id)

        if not requests:
            await query.message.reply_text("У вас нет входящих заявок.")
            # тут расширение ввода профиля
            return
        for r in requests:
            request_text = (
                f"- Тема: {r['topic']}\n"
                f"  От пользователя {r['sender_name']}\n\n"
            )
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Принять", callback_data=f"accept_request_{r['id']}"),
                    InlineKeyboardButton("Отклонить", callback_data=f"decline_request_{r['id']}")
                ]
            ])
            await query.message.reply_text(request_text, reply_markup=keyboard)
        return

    elif data == "outgoing_requests":
        requests = get_outgoing_requests(chat_id)

        if not requests:
            await query.message.reply_text("У вас нет отправленных заявок.")
            # тут расширение ввода профиля
            return
        for r in requests:
            request_text = (
                f"- Тема: {r['topic']}\n"
                f"  Пользователю {r['receiver_name']}\n\n"
            )
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Удалить", callback_data=f"delete_request_{r['id']}"),
                    InlineKeyboardButton("Напомнить", callback_data=f"remind_request_{r['id']}")
                ]
            ])
            await query.message.reply_text(request_text, reply_markup=keyboard)
        return
    elif data.startswith("accept_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        respond_request(request_id)

        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=f"Заявка принята, удачной работы в совместном проекте! "
                 f"Найдите его в разделе /projects."
        )
        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text=f"✅ Ваша заявка для {sender_info['full_name']} принята! "
                 f"Можете увидеть совместный проект в разделе /projects."
        )
    elif data.startswith("decline_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        respond_request(request_id)

        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text="Заявка успешно отклонена."
        )
        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text=f"❌ Ваша заявка для {sender_info['full_name']} отклонена. "
                 f"Не расстраивайтесь, попробуйте подобрать более подходящего партнера в /search!"
        )
    elif data.startswith("delete_request_"):
        request_id = int(data.split("_")[-1])
        respond_request(request_id)
        await query.message.reply_text("Заявка удалена. Можете найти нового кандидата для проекта.")

    elif data.startswith("remind_request_"):
        request_id = int(data.split("_")[-1])
        sender_id, receiver_id = get_request_users(request_id)
        sender_info = get_user_by_id(sender_id)
        receiver_info = get_user_by_id(receiver_id)

        await context.bot.send_message(
            chat_id=sender_info["telegram_id"],
            text="Напоминание отправлено! Ожидайте ответа."
        )
        await context.bot.send_message(
            chat_id=receiver_info["telegram_id"],
            text=f"🔔 Заявка от {sender_info['full_name']} ждёт вашего решения. "
                 f"Чтобы просмотреть все заявки, введите /view_requests."
        )