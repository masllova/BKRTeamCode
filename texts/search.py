from texts.stage import TEACHER_STAGE_NAMES, STUDENT_STAGE_NAMES

SEARCH_TEACHER = "Введите ФИО или ключевые слова для поиска научного руководителя"
SEARCH_STUDENT = "Введите ФИО или ключевые слова для поиска студента"
NOTHING_FOUND = "Ничего не найдено.\nПопробуйте уточнить запрос"
SEARCH_FINISHED = "Поиск завершён.\nВыберите нужный раздел из меню:"
CHOOSE_ACTION = "Выберите действие после того, как закончите работу с текущим списком кандидатов"
NEW_REQUESTS = "📩 Вы получили новую заявку.\nТема проекта: {text}\nЧтобы просмотреть заявки, введите команду /view_requests.\nТакже Вы сможете ознакомиться с заявками в любое удобное время через меню"
REQUESTS_HAS_BEEN_SENDED = "Всё готово! Ваша заявка успешно отправлена"
ERROR_WITH_REQUEST = "⚠ Не удалось создать заявку или отправить уведомление. Попробуйте позже"
REQUEST_ALREADY_SENDED = "\n❗️ Заявка уже отправлена"
ENTER_TOPIC = "Пожалуйста, введите название темы для совместного проекта.\nЕё будет видно в заявке для {name}"


def format_user_profile(
    full_name: str | None = None,
    role: str | None = None,
    stage: str | None = None,
    university: str | None = None,
    faculty: str | None = None,
    department: str | None = None,
    specialty: str | None = None,
    degree: str | None = None,
    articles: str | None = None,
    research_interests: str | None = None,
    email: str | None = None
) -> str:
    parts = ""

    if full_name and full_name.strip():
        parts += f"👤 {full_name.strip()}\n"
    if university and university.strip():
        parts += f"🏛 Университет: {university.strip()}\n"
    if stage and stage.strip():
        stage_key = stage.strip()
        if role and role.strip().lower() == "student":
            stage_name = STUDENT_STAGE_NAMES.get(stage_key, stage_key)
            parts += f"📚 Ступень образования: {stage_name}\n"
        else:
            stage_name = TEACHER_STAGE_NAMES.get(stage_key, stage_key)
            parts += f"📚 Научная/Преподавательская должность: {stage_name}\n"
    if faculty and faculty.strip():
        parts += f"Факультет: {faculty.strip()}\n"
    if department and department.strip():
        parts += f"Кафедра: {department.strip()}\n"
    if specialty and specialty.strip():
        parts += f"Специальность: {specialty.strip()}\n"
    if degree and degree.strip():
        parts += f"Степень: {degree.strip()}\n"
    if articles and articles.strip():
        parts += f"Статьи: {articles.strip()}\n"
    if research_interests and research_interests.strip():
        parts += f"Научные интересы: {research_interests.strip()}\n"
    if email and email.strip():
        parts += f"Почта: {email.strip()}\n"
    return parts