from telegram import InlineKeyboardButton, InlineKeyboardMarkup

SELECT_SETTINGS_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Профиль", callback_data=f"profile")],
        [InlineKeyboardButton("Уведомления", callback_data=f"notification")]
    ]
)

def make_student_settings_keyboard(has_faculty, has_department, has_specialty, has_articles, has_interests, has_email):
    edit_buttons = []
    add_buttons = []

    edit_buttons.append([InlineKeyboardButton("Ступень образования", callback_data=f"student_stage")])
    edit_buttons.append([InlineKeyboardButton("Учебное заведение", callback_data=f"student_university")])

    if has_faculty:
        edit_buttons.append([InlineKeyboardButton("Факультет", callback_data=f"student_faculty")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить факультет", callback_data=f"student_faculty")])
    if has_department:
        edit_buttons.append([InlineKeyboardButton("Кафедра/Направление", callback_data=f"student_department")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить кафедра/направление", callback_data=f"student_department")])
    if has_specialty:
        edit_buttons.append([InlineKeyboardButton("Специальность", callback_data=f"student_specialty")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить специальность", callback_data=f"student_specialty")])
    if has_articles:
        edit_buttons.append([InlineKeyboardButton("Статьи", callback_data=f"articles")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить cтатьи", callback_data=f"articles")])
    if has_interests:
        edit_buttons.append([InlineKeyboardButton("Научные интересы", callback_data=f"research_interests")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить научные интересы", callback_data=f"research_interests")])
    if has_email:
        edit_buttons.append([InlineKeyboardButton("Почта", callback_data=f"email")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить почту", callback_data=f"email")])

    return InlineKeyboardMarkup(edit_buttons + add_buttons + make_back_button("settings"))

def make_teacher_settings_keyboard(has_degree, has_articles, has_interests, has_email):
    edit_buttons = []
    add_buttons = []

    edit_buttons.append([InlineKeyboardButton("Должность", callback_data=f"teacher_stage")])
    edit_buttons.append([InlineKeyboardButton("Научное учреждение", callback_data=f"teacher_university")])

    if has_degree:
        edit_buttons.append([InlineKeyboardButton("Степень", callback_data=f"teacher_degree")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавть степень", callback_data=f"teacher_degree")])
    if has_articles:
        edit_buttons.append([InlineKeyboardButton("Статьи", callback_data=f"articles")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить cтатьи", callback_data=f"articles")])
    if has_interests:
        edit_buttons.append([InlineKeyboardButton("Научные интересы", callback_data=f"research_interests")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить научные интересы", callback_data=f"research_interests")])
    if has_email:
        edit_buttons.append([InlineKeyboardButton("Почта", callback_data=f"email")])
    else:
        add_buttons.append([InlineKeyboardButton("Добавить почта", callback_data=f"email")])
    return InlineKeyboardMarkup(edit_buttons + add_buttons + make_back_button("settings"))

def make_back_button(command):
    return [InlineKeyboardButton("Назад", callback_data=f"{command}")]