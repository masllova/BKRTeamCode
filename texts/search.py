SEARCH_TEACHER = "Введите ФИО или ключевые слова для поиска научного руководителя."
SEARCH_STUDENT = "Введите ФИО или ключевые слова для поиска студента."
NOTHING_FOUND = "Ничего не найдено.\nПопробуйте уточнить запрос."
SEARCH_FINISHED = "Поиск завершён.\nВыберите нужный раздел из меню:"
CHOOSE_ACTION = "Выберите действие:"

def format_user_profile(
    full_name: str | None = None,
    role: str | None = None,
    stage: str | None = None,
    university: str | None = None,
    faculty: str | None = None,
    department: str | None = None,
    articles: str | None = None,
    research_interests: str | None = None,
) -> str:
    parts = ""

    if full_name and full_name.strip():
        parts += f"👤 {full_name.strip()}\n"
    if role and role.strip():
        parts += f"🎓 Роль: {role.strip()}\n"
    if university and university.strip():
        parts += f"🏛 Университет: {university.strip()}\n"
    if stage and stage.strip():
        if role and role.strip().lower() == "student":
            parts += f"📚 Ступень образования: {stage.strip()}\n"
        else:
            parts += f"📚 Научная/Преподавательская должность: {stage.strip()}\n"
        parts += f"Факультет: {faculty.strip()}\n"
    if department and department.strip():
        parts += f"Кафедра: {department.strip()}\n"
    if articles and articles.strip():
        parts += f"Статьи: {articles.strip()}\n"
    if research_interests and research_interests.strip():
        parts += f"Интересы: {research_interests.strip()}\n"

    return parts