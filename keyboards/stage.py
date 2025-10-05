from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STUDENT_STAGES = InlineKeyboardMarkup([
    [InlineKeyboardButton("Бакалавриат", callback_data="bachelor")],
    [InlineKeyboardButton("Специалитет", callback_data="specialist")],
    [InlineKeyboardButton("Магистратура", callback_data="master")],
    [InlineKeyboardButton("Аспирантура", callback_data="phd")],
    [InlineKeyboardButton("Другое", callback_data="other")]
])

TEACHER_STAGES = InlineKeyboardMarkup([
    [InlineKeyboardButton("Преподаватель", callback_data="teacher")],
    [InlineKeyboardButton("Старший преподаватель", callback_data="senior_teacher")],
    [InlineKeyboardButton("Доцент", callback_data="associate_professor")],
    [InlineKeyboardButton("Профессор", callback_data="professor")],
    [InlineKeyboardButton("Другое", callback_data="other")]
])