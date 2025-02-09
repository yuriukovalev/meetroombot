# 1. Используем Python 3.11
FROM python:3.11

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Устанавливаем часовой пояс (Екатеринбург)
ENV TZ=Asia/Yekaterinburg

# 4. Копируем файлы проекта
COPY requirements.txt .
COPY bot.py .
COPY data.py .
COPY .env .

# 5. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Запускаем бота
CMD ["python", "bot.py"]