from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

requests_state = {}

async def handle_requests_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return