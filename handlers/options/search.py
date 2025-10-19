import traceback
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_users import get_user_role, search_users
from db.queries_requests import add_request
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER, NOTHING_FOUND, SEARCH_FINISHED, CHOOSE_ACTION, format_user_profile
from keyboards.search import SEARCH_RETRY_BUTTON, SEARCH_EXIT_BUTTON, SEARCH_MORE_BUTTON, request_button
from keyboards.menu import get_menu_keyboard
from db.queries_users import get_user_by_chat_id, get_user_role

search_state: dict[int, dict] = {}

async def handle_search_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if all(v is None for v in search_state.get(chat_id).values()):
        user_role = get_user_role(chat_id)
        target_role = "teacher" if user_role == "student" else "student"

        search_state[chat_id] = {
            "query": text,
            "last_id": None,
            "target_role": target_role
        }
    elif search_state.get(chat_id, {}).get("query", "").startswith("awaiting_topic_for_request_"):
        state_info = search_state[chat_id] 
        target_id_str = state_info["query"].replace("awaiting_topic_for_request_", "")
        target_id = int(target_id_str)

        try:
            add_request(sender_id=chat_id, receiver_id=target_id, topic=text)

            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"📩 Вы получили новую заявку.\n"
                    f"Тема проекта: {text}\n"
                    "Чтобы просмотреть заявки, введите команду /view_requests.\n"
                    "Вы сможете ознакомиться с заявками в любое удобное время через меню."
                )
            )
            keyboard = get_menu_keyboard(get_user_role(chat_id))
            await update.message.reply_text(
                "Всё готово! Ваша заявка успешно отправлена.", 
                reply_markup=keyboard
            )
            search_state.pop(chat_id, None)

        except Exception as e:
            # Печатаем полную информацию об ошибке в консоль
            print("Ошибка при создании заявки или отправке сообщения:")
            traceback.print_exc()
            
            # Сообщение пользователю
            await update.message.reply_text(
                "⚠ Не удалось создать заявку или отправить уведомление. Попробуйте позже."
            )
        return

    query_text = search_state[chat_id]["query"]
    last_id = search_state[chat_id]["last_id"]
    target_role = search_state[chat_id]["target_role"]
    users = search_users(query_text, target_role, last_id)

    if not users:
        keyboard = InlineKeyboardMarkup([SEARCH_RETRY_BUTTON, SEARCH_EXIT_BUTTON])
        await update.message.reply_text(NOTHING_FOUND, reply_markup=keyboard)
        return
    search_state[chat_id]["last_id"] = users[-1]["id"] if len(users) == 3 else None

    for u in users:
        text_card = format_user_profile(
            full_name=u['full_name'],
            role=u['role'],
            stage=u['stage'],
            university=u['university'],
            faculty=u['faculty'],
            department=u['department'],
            articles=u['department'],
            research_interests=u['research_interests']
        )
        keyboard = InlineKeyboardMarkup([request_button(u['telegram_id'])])
        await update.message.reply_text(text_card, reply_markup=keyboard)

    buttons = []

    if search_state[chat_id]["last_id"]:
        buttons.append([SEARCH_MORE_BUTTON])

    buttons.append(SEARCH_RETRY_BUTTON)
    buttons.append(SEARCH_EXIT_BUTTON)

    await update.message.reply_text(CHOOSE_ACTION, reply_markup=InlineKeyboardMarkup(buttons))

async def handle_search_callback(update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data

    if data == "search_exit":
        role = get_user_role(chat_id)
        keyboard = get_menu_keyboard(role)
        await query.message.reply_text(SEARCH_FINISHED, reply_markup=keyboard)
        search_state.pop(chat_id, None)
        return
    elif data.startswith("request_"):
        target_id = int(data.split("_")[1])
        target_user = get_user_by_chat_id(target_id)

        search_state[chat_id] = {
            "query": f"awaiting_topic_for_request_{target_id}",
            "last_id": None,
            "target_role": None
        }
        await query.message.reply_text(
            f"Пожалуйста, введите название темы для совместного проекта.\n"
            f"Её будет видно в заявке для {target_user['full_name']}"
        )
        return
    elif data == "search_retry":
        role = get_user_role(chat_id)

        if role == "student":
            await query.message.reply_text(SEARCH_TEACHER)
        else:
            await query.message.reply_text(SEARCH_STUDENT)

        search_state[chat_id] = {
            "query": None,
            "last_id": None,
            "target_role": None
        }
        return
    elif data == "search_more":
        fake_update = Update(update.update_id, message=update.callback_query.message)
        await handle_search_text(fake_update, context)
        return