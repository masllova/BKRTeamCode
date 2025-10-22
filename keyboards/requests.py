from telegram import InlineKeyboardButton
ACCEPT_BUTTON = InlineKeyboardButton("Принять", callback_data="accept_request")
DECLINE_BUTTON = InlineKeyboardButton("Отклонить", callback_data="decline_request")
DELETE_BUTTON = InlineKeyboardButton("Удалить", callback_data="delete_request")
REMIND_BUTTON = InlineKeyboardButton("Напомнить", callback_data="remind_request")
