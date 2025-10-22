from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from db.queries_groups import get_group_by_id
from db.queries_users import get_user_group_ids

qroups_state = {}

async def projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    group_ids = get_user_group_ids(chat_id)

    if not group_ids:
        await update.message.reply_text(
            "У тебя пока нет проектов.\n"
            "/search - Найти претендента на общий проект\n"
            "/requests - Посмотреть заявки"
        )
        return

    buttons = []

    for gid in group_ids:
        group = get_group_by_id(gid)
        if group:
            buttons.append([
                    InlineKeyboardButton(
                    text=group["name"],
                    callback_data=f"project_{gid}"
                )]
            )

    text = "Выбери проект:"
    keyboard = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(text, reply_markup=keyboard)
    return

async def handle_projects_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return

async def handle_projects_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return