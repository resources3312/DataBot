import os
from telebot import TeleBot
from telebot import types
import telebot
import sqlite3
from dotenv import load_dotenv
from time import sleep
from datetime import datetime
load_dotenv()

bot = TeleBot(os.getenv("TOKEN"))

def check_users(msg: message) -> bool:
    try:    
        with sqlite3.connect("database.db") as db:
            db.cursor().execute(f"SELECT username FROM users")
            if msg.from_user.username not in db.cursor().fetchall():
                db.cursor().execute(f"INSERT INTO intrested (tgid, username, last_name, first_name, time), 
                VALUES ({str(msg.from_user.id)}, {msg.from_user.username}, {msg.from_user.last_name}, {msg.from_user.first_name}, {' '.join(str(datetime.now()).split(".")[:-1])})")
                db.commit()
                bot.send_message(message.chat.id, "Доступ запрещен, если ваше намерение уничтожить приватность как понятие чисто свяжитесь с поддержкой")
                return False
            else:
                return True
    except sqlite3.Error:
        bot.send_message(message.chat.id, "Ошибка на стороне сервера, попробуйте позже или свяжитесь с поддержкой")

def get_db_data(table: str, option: str, value: str):
    try:
        with sqlite.connect("database.db") as db:
            db.cursor().execute(f"SELECT * FROM {table} WHERE {option}={value}")
            data = db.cursor().fetchall()
            return {"name": data[1] if data[1] != '' else: "Не найдено",
                    "born": data[2] if data[2] != '' else: "Не найдено",
                    "number": data[3] if data[3] != '' else: "Не найдено",
                    "email": data[4] if data[4] != '' else: "Не найдено",
                    "tgid": data[5] if data[5] != '' else: "Не найдено",
                    "tgun": data[6] if data[6] != '' else: "Не найдено",
                    "vkid": data[7] if data[7] != '' else: "Не найдено",
                    "okid": data[8] if data[8] != '' else: "Не найдено",
                    "instid": data[9] if data[9] != '' else: "Не найдено",
                    "fbid": data[10] if data[10] != '' else: "Не найдено",
                    "snpas": data[11] if data[11] != '' else: "Не найдено",
                    "inn": data[12] if data[12] != '' else: "Не найдено", 
                    "snils": data[13] if data[13] != '' else: "Не найдено",
                    "card": data[14] if data[14] != '' else: "Не найдено",
                    "addr": data[15] if data[15] != '' else: "Не найдено",
                    "org": data[16] if data[16] != '' else: "Не найдено"}
    except sqlite3.Error:
        return False


def get_report(data: dict) -> str:
    return f""" 
<b>✅Отчет по вашему запросу:</b>
    
👤 <b>ФИО:</b> <code>{data['name']}</code>
    
🏥 <b>Дата рождения:</b> <code>{data['born']}</code>

📞 <b>Номера телефона:</b> <code>{data['number']}</code>

📧 <b>Электронные почты:</b> <code>{data['email']}</code>

🌐 <b>Соцсети:</b>
    |    
    |- <b>Telegram:</b> <code>{data['tgid']}</code>
    |    
    |- <b>Instagram:</b> <code>{data["instid"]}</code>

        

❗Если у вас имеются вопросы связанные с работой бота, или есть желание внести свою лепту в уничтожение приватности как понятия т.е 
  дополнить базу данных, пишите в нашу поддержку
"""


@bot.message_handler(commands=["start"])
def get_start(message):
    if check_users(): 
        bot.send_message(message.chat.id, "Тебя приветствует DataBot, введи запрос в нижеуказанном формате для получения данных")
        bot.send_message(message.chat.id, "Справка")

@bot.message_handler(commands=["help"])
def get_manual(message):
    if check_users():
        msg = bot.send_message(message.chat.id, "")
@bot.message_handler(content_types=["text"])
def handler(message):
    if check_users():
        elif len(message.text) == 11:
            msg = bot.send_message(message.chat.id, "Пожалуйста подождите, идет поиск по базе данных.. ")
            bot.edit_message_text(get_report(get_db_data("people", "number", message.text)), chat_id=message.chat.id,
            message_id=msg.message_id, parse_mode="html")
        elif "@" in message.text and "." in message.text:
            msg = bot.send_message(message.chat.id, "Пожалуйста подождите, идет поиск по базе данных.. ")
            bot.edit_message_text(get_report(get_db_data("people", "email", message.text)), chat_id=message.chat.id,
            message_id=msg.message_id, parse_mode="html")
        elif "@" in message.text:
            msg = bot.send_message(message.chat.id, "Пожалуйста подождите, идет поиск по базе данных.. ")
            bot.edit_message_text(get_report(get_db_data("people", "tgun", message.text)), chat_id=message.chat.id,
            message_id=msg.message_id, parse_mode="html")
        elif "vk.com" in message.text:

def main():
    bot.infinity_polling()

if __name__ == '__main__':
    main()
