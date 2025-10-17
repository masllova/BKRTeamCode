from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_users import get_user_role, search_users
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER
from keyboards.search import REQUEST_BUTON, SEARCH_MORE_BUTTON, BACK_BUTTON
from keyboards.menu import get_menu_keyboard
from db.queries_users import get_user_by_chat_id

search_state: dict[int, dict] = {}

async def handle_search_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()

    if search_state.get(chat_id, {}).get("state") != "searching_results":
        user_role = get_user_role(chat_id)
        target_role = "teacher" if user_role == "student" else "student"

        search_state[chat_id] = {
            "state": "searching_results",
            "query": text,
            "last_id": None,
            "target_role": target_role
        }

    query_text = search_state[chat_id]["query"]
    last_id = search_state[chat_id]["last_id"]
    target_role = search_state[chat_id]["target_role"]
    users = search_users(query_text, target_role, last_id)

    if not users:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔎 Новый поиск", callback_data="search_retry")],
            [InlineKeyboardButton("🏠 Выйти в меню", callback_data="search_exit")]
        ])
        await update.message.reply_text(
            "😕 Ничего не найдено.\nПопробуйте уточнить запрос.",
            reply_markup=keyboard
        )
        return
    search_state[chat_id]["last_id"] = users[-1]["id"] if len(users) == 3 else None

    for u in users:
        text_card = (
            f"────────────────\n"
            f"👤 {u['full_name']}\n"
            f"🎓 Роль: {u['role']}\n"
            f"🏛 Университет: {u['university'] or '-'}\n"
            f"📚 Уровень: {u['stage'] or '-'}\n"
            f"Факультет: {u['faculty'] or '-'}\n"
            f"Кафедра: {u['department'] or '-'}\n"
            f"Статьи: {u['articles'] or '-'}\n"
            f"Интересы: {u['research_interests'] or '-'}\n"
            f"────────────────"
        )
        keyboard = InlineKeyboardMarkup([[REQUEST_BUTON]])
        await update.message.reply_text(text_card, reply_markup=keyboard)

    buttons = []

    if search_state[chat_id]["last_id"]:
        buttons.append([SEARCH_MORE_BUTTON])

    buttons.append([InlineKeyboardButton("Новый поиск", callback_data="search_retry")])
    buttons.append([InlineKeyboardButton("Выйти в меню", callback_data="search_exit")])

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def handle_search_query_callback(update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data
    user = get_user_by_chat_id(chat_id)

    if data == "search_exit":
        keyboard = get_menu_keyboard(user["role"])
        await query.edit_message_reply_markup(reply_markup=keyboard)
        search_state.pop(chat_id, None)
        return

    elif data == "search_retry":
        role = get_user_role(chat_id)
        if role == "student":
            await query.message.reply_text(SEARCH_STUDENT)
        else:
            await query.message.reply_text(SEARCH_TEACHER)
        search_state[chat_id] = {
            "state": "awaiting_search_query",
            "query": None,
            "last_id": None,
            "target_role": None
        }
        return

async def handle_searching_results_callback(update, context):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id
    data = query.data
    user = get_user_by_chat_id(chat_id)

    if data.startswith("request_"):
        target_id = int(data.split("_")[1])
        # to do: логика отправки заявки
        print("Заявка отправлена", target_id)
        return

    elif data == "search_more":
        await handle_search_text(update, context)
        return

    elif data == "search_exit":
        keyboard = get_menu_keyboard(user["role"])
        await query.edit_message_reply_markup(reply_markup=keyboard)
        search_state.pop(chat_id, None)
        return