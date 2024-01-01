import telebot
from telebot import types
import requests
import json
# import SQLite3
bot = telebot.TeleBot('6639915150:AAESXmXwGP04nXgQnknc9jXdTGdnP5mSExg')
API = 'f9663ef9687eeb6f2c4fda2d986ddd22'


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Хочу дізнатися погоду')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Інстаграм автора')
    btn3 = types.KeyboardButton('Телеграм автора')
    markup.row(btn2,btn3)
    bot.send_message(message.chat.id, 'Привіт', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

@bot.message_handler(func=lambda message: True)
def on_click(message):
    if message.text == 'Телеграм автора':
        bot.send_message(message.chat.id, 'https://t.me/Dan_Pavlo')
    elif message.text == 'Інстаграм автора':
        bot.send_message(message.chat.id, 'https://www.instagram.com/pavlo_danylkiv/')
    elif message.text == 'Хочу дізнатися погоду':
        bot.send_message(message.chat.id, 'Будь ласка, введіть назву міста для отримання інформації про погоду:')
        bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:

        data = json.loads(res.text)
        temperature = data["main"]["temp"]
        bot.reply_to(message, f'Зараз погода: {temperature} градусів за цельсієм')

        imagine = 'img.png' if temperature > 5.0 else 'img_1.png'
        file = open('./' + imagine, 'rb')
        bot.send_photo(message.chat.id,file)
    else:
        bot.reply_to(message, 'Назва міста вказана невірно')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привіт! {message.from_user.first_name}')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'хто створив цього бота?':
        bot.send_message(message.chat.id, 'https://t.me/Dan_Pavlo')

bot.polling(none_stop=True)