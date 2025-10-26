from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def make_settings_keyboard(role):
    buttons = []

    if role == "student":
        buttons.append([InlineKeyboardButton("Ступень образование", callback_data=f"student_stage")])
        buttons.append([InlineKeyboardButton("Учебное заведение", callback_data=f"student_university")])
        buttons.append([InlineKeyboardButton("Факультет", callback_data=f"student_faculty")])
        buttons.append([InlineKeyboardButton("Кафедра/Направление", callback_data=f"student_departament")])
        buttons.append([InlineKeyboardButton("Специальность", callback_data=f"student_specialty")])
    else:
        buttons.append([InlineKeyboardButton("Должность", callback_data=f"teacher_stage")])
        buttons.append([InlineKeyboardButton("Научное учреждение", callback_data=f"teacher_university")])
        buttons.append([InlineKeyboardButton("Степень", callback_data=f"teacher_degree")])
    buttons.append([InlineKeyboardButton("Статьи", callback_data=f"articles")])
    buttons.append([InlineKeyboardButton("Научные интересы", callback_data=f"research_interests")])
    return InlineKeyboardMarkup(buttons)