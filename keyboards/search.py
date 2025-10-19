from telegram import InlineKeyboardButton

SEARCH_RETRY_BUTTON = [InlineKeyboardButton("Новый поиск", callback_data="search_retry")]
SEARCH_EXIT_BUTTON = [InlineKeyboardButton("Выйти в меню", callback_data="search_exit")]
SEARCH_MORE_BUTTON = InlineKeyboardButton("Показать ещё", callback_data="search_more")
def request_button(chat_id):
    return [InlineKeyboardButton("Отправить заявку", callback_data=f"request_{chat_id}")]