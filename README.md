# 🤖 MeetRoomBot — Телеграм-бот для разблокировки переговорных

**MeetRoomBot** — это Telegram-бот, который помогает **разблокировать переговорные комнаты** в офисах компании.  
Он использует **Docker + Aiogram + FSM**, а также логирует все действия пользователей.

## 🚀 **Особенности**
✅ Разблокировка переговорных по городам, офисам, этажам  
✅ Логирование входов и разблокировок в `bot_usage.log`  📌 Для macOS:

```bash
Копировать код
brew install docker docker-compose
2️⃣ Склонировать репозиторий
```bash
✅ Кнопки `"⬅️ Назад"` для удобного перемещения  
✅ **Работает в Docker**, легко развернуть  

---

## 🛠 **Как развернуть бота в Docker**
### 1️⃣ **Установить `Docker` и `Docker Compose` (если их нет)**
📌 **Для Ubuntu/Debian:**  
```bash
sudo apt update && sudo apt install docker docker-compose -y

```bash
git clone https://github.com/<username>/MeetRoomBot.git
cd MeetRoomBot

3️⃣ Настроить .env
Создаём файл .env (если его нет) и добавляем:

```bash
BOT_TOKEN=your_telegram_bot_token


🐳 Запуск бота в Docker

📌 Запустить бота
```bash
docker-compose up -d
📌 Контейнер запустится в фоновом режиме.

📌 Пересобрать и запустить заново
```bash
docker-compose up --build -d
📌 Если изменился код, пересборка используется после изменений в bot.py.

📌 Остановить бота
```bash
docker-compose down
🔍 Как проверить бота?

📌 Посмотреть запущенные контейнеры
bash
Копировать код
docker ps
📌 Просмотреть логи работы бота
bash
Копировать код
docker logs -f my_telegram_bot
📌 (-f показывает новые логи в реальном времени)

📁 Как посмотреть логи активности?

Логи хранятся в файле bot_usage.log.

Вывести последние 10 строк:

bash
Копировать код
tail -n 10 bot_usage.log
🔹 Или в боте отправить команду /logs.

🛠 Полезные команды

📌 Перезапустить контейнер
bash
Копировать код
docker restart my_telegram_bot
📌 Удалить ненужные образы и кеш
bash
Копировать код
docker system prune -af
📌 Запустить бота заново после остановки
bash
Копировать код
docker start my_telegram_bot
🎯 Теперь MeetRoomBot полностью готов к работе в Docker! 🚀

📌 Автор: @your_username

📌 Лицензия: MIT

📌 Разработка [Aiogram 3.0 + Python]

yaml
Копировать код

---

## 🎯 **Что теперь есть в `README.md`?**
✔ **Объяснение, что делает бот**  
✔ **Шаги по установке (`Docker`)**  
✔ **Как запустить (`docker-compose`)**  
✔ **Как просмотреть логи (`logs` + `tail -n 10 bot_usage.log`)**  
✔ **Полезные команды для Docker (`restart`, `prune`, `start`)**  

---

# 🚀 **Что дальше?**
1️⃣ Добавь `README.md` в GitHub:  
```bash
git add README.md
git commit -m "Добавил README.md"
git push origin main
2️⃣ Открой репозиторий на GitHub → README.md отобразится на главной странице

3️⃣ Проверь, всё ли работает → Пробуй команды в Docker
```bash
git clone https://github.com/yuriukovalev/MeetRoomBot.git
cd MeetRoomBot