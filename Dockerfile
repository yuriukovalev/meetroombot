# 1. Используем официальное изображение Python 3.11
FROM python:3.11

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файлы проекта в контейнер
COPY requirements.txt .
COPY bot.py .
COPY data.py .
COPY .env .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Запускаем бота
CMD ["python", "bot.py"]