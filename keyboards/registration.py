from telegram import InlineKeyboardButton, InlineKeyboardMarkup

ROLE_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("Студент", callback_data="student")],
    [InlineKeyboardButton("Преподаватель", callback_data="teacher")]
])