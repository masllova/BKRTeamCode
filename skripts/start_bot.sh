#!/bin/bash

PROJECT_DIR=~/VKRTeamBot
REPO_URL="https://github.com/masllova/VKRTeamCode"

echo "🚀 Запускаем код для VKRTeamBot..."

# Клонирование, если проекта ещё нет
if [ ! -d "$PROJECT_DIR" ]; then
    git clone $REPO_URL $PROJECT_DIR
fi

cd $PROJECT_DIR || exit
git pull

# Виртуальное окружение
if [ ! -d "venv" ]; then
    echo "⚙️ Создаём виртуальное окружение..."
    python3 -m venv venv
    echo "✔️ Виртуальное окружение создано!"
fi

echo "⚙️ Активируем виртуальное окружение..."
source venv/bin/activate

pip install -r requirements.txt
echo "✔️ Зависимости установлены!"

# --- 🔐 Токен бота ---
if [ -z "$TELEGRAM_TOKEN" ]; then
    read -p "Введите токен бота: " BOT_TOKEN
    export TELEGRAM_TOKEN="$BOT_TOKEN"
fi

# --- 🔑 Пароль к БД ---
if [ -z "$VKR_DB_PASSWORD" ]; then
    read -s -p "Введите пароль к базе данных: " DB_PASSWORD
    echo ""
    export VKR_DB_PASSWORD="$DB_PASSWORD"
fi

# Запуск бота
echo "⚙️ Ещё немного..."
python main.py