from telegram import InlineKeyboardButton, InlineKeyboardMarkup
REQUEST_BUTON = InlineKeyboardButton("Отправить заявку", callback_data=f"request_{u['id']}")
SEARCH_MORE_BUTTON = InlineKeyboardButton("Показать ещё", callback_data="search_more")
BACK_BUTTON = InlineKeyboardButton("Выйти в меню", callback_data="menu")
