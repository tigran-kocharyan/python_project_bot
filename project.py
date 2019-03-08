from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import requests
import datetime
import os

up = Updater("728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
dp = up.dispatcher
job = up.job_queue

def start(bot, up):
    up.message.reply_text('Hello (*・ω・)ﾉ')
    bot.sendDocument(chat_id=up.message.chat_id, document='CAADAQAD4AEAAkWQ0AeCTzUa7LnRbQI')

def echo(bot, up):
    up.message.reply_text("Undefined ┐('～`;)┌")

def buttons():
    keys=[[InlineKeyboardButton('Tomorrow', callback_data='1'), InlineKeyboardButton('No, thanks!', callback_data='2')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)

def callback_time(bot, job):
    bot.send_message(chat_id=job.context, text='Beep!')
    
def repeat(bot, up, job_queue):
    job_queue.start()
    bot.send_message(chat_id=up.message.chat_id, text='Starting... (´• ω •`)')
    job_queue.run_repeating(callback_time, interval=7200, first=0, context=up.message.chat_id)

def get_callback_from_button(bot, up):
    query = up.callback_query
    username = up.effective_user.username
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    if int(query.data) == 1:
        query.answer()
        api='0f798fa08e77c5b4a2ad9d1bcbf5d700'
        try:
            settings = {'q': 'Tashkent', 'units': 'metric', 'lang': 'en', 'APPID': api}
            r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=settings)
            data=r.json()
            bot.sendMessage(chat_id=chat_id, text=f"Tomorrow's weather in Tashkent: {int(data['list'][1]['main']['temp_max'])}°C")
        except Exception as e:
            print("Exception (weather):", e)
            pass
    elif int(query.data) == 2:
        bot.sendMessage(chat_id=chat_id,text="You're welcome (^_~)")
        query.answer()                    

def weather(bot, up):
    api='0f798fa08e77c5b4a2ad9d1bcbf5d700'
    try:
        settings = {'q': 'Tashkent', 'units': 'metric', 'lang': 'en', 'APPID': api}
        r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=settings)
        data=r.json()
        bot.sendMessage(chat_id=up.message.chat_id, text=f"Current weather in Tashkent: {int(data['list'][0]['main']['temp_max'])}°C", reply_markup=buttons())
    except Exception as e:
        print("Exception (weather):", e)
        pass

dp = up.dispatcher
start = CommandHandler("start", start)
weather = CommandHandler("weather", weather)
repeat = CommandHandler("repeat", repeat, pass_job_queue=True)
dp.add_handler(start)
dp.add_handler(weather)
dp.add_handler(repeat)
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(CallbackQueryHandler(get_callback_from_button))

#webhook settings
PORT = int(os.environ.get('PORT', '5000'))
TOKEN="728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4"
up.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
up.bot.set_webhook("https://project-py-bot.herokuapp.com/728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")

up.idle()
