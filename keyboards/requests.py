from telegram import InlineKeyboardButton

def build_incoming_keyboard(id: int):
    return [[
        InlineKeyboardButton("Принять", callback_data=f"accept_request_{id}"), 
        InlineKeyboardButton("Отклонить", callback_data=f"decline_request_{id}")
        ]]

def build_outgoing_keyboard(id: int):
    return [[
        InlineKeyboardButton("Удалить", callback_data=f"delete_request_{id}"), 
        InlineKeyboardButton("Напомнить", callback_data=f"remind_request_{id}")
        ]]
