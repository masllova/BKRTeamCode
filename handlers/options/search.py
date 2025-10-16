from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from db.queries_users import get_user_role, search_users
from handlers.options.menu import menu_state
from texts.search import SEARCH_STUDENT, SEARCH_TEACHER
from keyboards.search import REQUEST_BUTON, SEARCH_MORE_BUTTON, BACK_BUTTON

search_state: dict[int, dict] = {}

async def handle_search_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    role = await get_user_role(chat_id)

    if role == "student":
        await update.message.reply_text(SEARCH_STUDENT)
    else:
        await update.message.reply_text(SEARCH_TEACHER)
    return

async def handle_search_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text.strip()
    state = search_state.get(chat_id, {})
    
    if state.get("state") != "searching_results":
        user_role = get_user_role(chat_id)
        target_role = "teacher" if user_role == "student" else "student"

        search_state[chat_id] = {
            "state": "searching_results",
            "query": text,
            "last_id": None,
            "target_role": target_role
        }

    query = search_state[chat_id]["query"]
    last_id = search_state[chat_id]["last_id"]
    target_role = search_state[chat_id]["target_role"]

    users = search_users(query, target_role, last_id)

    if not users:
        keyboard = InlineKeyboardMarkup([[BACK_BUTTON
]])
        await update.message.reply_text(
            "❌ Пользователи не найдены.",
            reply_markup=keyboard
        )
        search_state.pop(chat_id, None)
        return

    search_state[chat_id]["last_id"] = users[-1]["id"] if len(users) == 5 else None

    for u in users:
        text_card = (
            f"────────────────────\n"
            f"👤 {u['full_name']}\n"
            f"🎓 Роль: {u['role']}\n"
            f"🏛 Университет: {u['university'] or '-'}\n"
            f"📚 Уровень: {u['stage'] or '-'}\n"
            f"Факультет: {u['faculty'] or '-'}\n"
            f"Кафедра: {u['department'] or '-'}\n"
            f"Статьи: {u['articles'] or '-'}\n"
            f"Интересы: {u['research_interests'] or '-'}\n"
            f"────────────────────"
        )

        keyboard = InlineKeyboardMarkup([[REQUEST_BUTON]])
        await update.message.reply_text(text_card, reply_markup=keyboard)

    last_buttons = []
    if menu_state[chat_id]["last_id"]:
        last_buttons.append(SEARCH_MORE_BUTTON)
    last_buttons.append(BACK_BUTTON)

    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=InlineKeyboardMarkup([last_buttons])
    )