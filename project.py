from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import datetime
import os

up = Updater("728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
dp = up.dispatcher

def start(bot, up):
    up.message.reply_text('Hello (*・ω・)ﾉ')
    bot.sendDocument(chat_id=up.message.chat_id, document='CAADAQAD4AEAAkWQ0AeCTzUa7LnRbQI')

def echo(bot, up):
    up.message.reply_text("Undefined ┐('～`;)┌")

def weather(bot, up):
    api='0f798fa08e77c5b4a2ad9d1bcbf5d700'
    try:
        settings = {'q': 'Tashkent', 'units': 'metric', 'lang': 'en', 'APPID': api}
        r = requests.get('http://api.openweathermap.org/data/2.5/weather', params=settings)
        data=r.json()
        bot.sendMessage(chat_id=up.message.chat_id, text=f"Weather in Tashkent: {int(data['main']['temp_max'])}°C")
    except Exception as e:
        print("Exception (weather):", e)
        pass

dp = up.dispatcher
start = CommandHandler("start", start)
weather = CommandHandler("weather", weather)
dp.add_handler(start)
dp.add_handler(weather)
dp.add_handler(MessageHandler(Filters.text, echo))

#webhook settings
PORT = int(os.environ.get('PORT', '5000'))
TOKEN="728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4"
up.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
up.bot.set_webhook("https://project-py-bot.herokuapp.com/728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
                        
#up.start_polling()
up.idle()
