#!/bin/bash

PROJECT_DIR=~/VKRTeamBot
REPO_URL="https://github.com/masllova/VKRTeamCode"

echo "🚀 Запускаем код для VKRTeamBot..."

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

# Токен бота
if [ -z "$TELEGRAM_TOKEN" ]; then
    read -p "Введите токен бота: " BOT_TOKEN
    export TELEGRAM_TOKEN="$BOT_TOKEN"
fi

# Запуск бота
echo "⚙️ Ещё немного"
python main.py