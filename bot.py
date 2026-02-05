import os
import telebot
import os
from flask import Flask
from threading import Thread

app = Flask(__name__)

@app.get("/")
def home():
    return "ok", 200

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run_web, daemon=True).start()

from telebot import types

BOT_TOKEN = os.getenv("BOT_TOKEN")  # <-- токен придёт из Render
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(BOT_TOKEN)


STEAM_SALE_URL = "https://gglead.org/ggsel3/?flow=11078&ulp=https%3A%2F%2Fggsel.com%2Fcatalog%2Fsales"
GAMES_URL = "https://gglead.org/ggsel3/?flow=11075&ulp=https%3A%2F%2Fggsel.com%2Fcatalog%2Figry-po-nazvaniyu"
STEAM_TOPUP_URL = "https://gglead.org/ggsel3/?flow=11076&ulp=https%3A%2F%2Fggsel.com%2Fsearch%2F%D0%BF%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%D0%B8%D0%B5%2520%D1%81%D1%82%D0%B8%D0%BC"

USERS_FILE = "users.txt"

bot = telebot.TeleBot(BOT_TOKEN)


def save_user(user_id: int):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write(f"{user_id}\n")
        return

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        users = set(line.strip() for line in f if line.strip())

    if str(user_id) not in users:
        with open(USERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{user_id}\n")


def get_user_count() -> int:
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())


@bot.message_handler(commands=["start"])
def start(message):
    save_user(message.from_user.id)
    count = get_user_count()

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(types.InlineKeyboardButton("🔥 Скидки Steam до 70%", url=STEAM_SALE_URL))
    kb.add(types.InlineKeyboardButton("🎮 Игры по названию", url=GAMES_URL))
    kb.add(types.InlineKeyboardButton("💳 Пополнение Steam", url=STEAM_TOPUP_URL))

    bot.send_message(
        message.chat.id,
        f"🔥 Выбери раздел:\n\n👥 Пользователей в боте: {count}",
        reply_markup=kb
    )


@bot.message_handler(commands=["users"])
def users(message):
    bot.send_message(message.chat.id, f"👥 Пользователей в боте: {get_user_count()}")


if __name__ == "__main__":
    bot.infinity_polling(timeout=30, long_polling_timeout=30)

