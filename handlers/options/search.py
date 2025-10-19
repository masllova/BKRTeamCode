from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_users import get_user_role, search_users
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER, NOTHING_FOUND, SEARCH_FINISHED, CHOOSE_ACTION, format_user_profile
from keyboards.search import SEARCH_RETRY_BUTTON, SEARCH_EXIT_BUTTON, SEARCH_MORE_BUTTON, request_button
from keyboards.menu import get_menu_keyboard
from db.queries_users import get_user_by_chat_id

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
        keyboard = InlineKeyboardMarkup([request_button(chat_id)])
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
    user = get_user_by_chat_id(chat_id)

    if data == "search_exit":
        keyboard = get_menu_keyboard(user["role"])
        await query.message.reply_text(SEARCH_FINISHED, reply_markup=keyboard)
        search_state.pop(chat_id, None)
        return
    elif data.startswith("request_"):
        target_id = int(data.split("_")[1])
        
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    "📩 Вы получили новую заявку.\n"
                    "Чтобы просмотреть её, введите команду /view_requests.\n"
                    "Вы сможете ознакомиться с заявками в любое удобное время через меню."
                )
            )
        except Exception:
            await update.callback_query.message.reply_text(
                "⚠ Не удалось отправить уведомление пользователю. Попробуйте позже."
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
        fake_update = Update(
            update.update_id,
            message=update.callback_query.message
        )
        await handle_search_text(fake_update, context)
        return