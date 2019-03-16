from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import requests
import datetime
import telegram
import psycopg2 as sql
import os

up = Updater("728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
dp = up.dispatcher
bd = sql.connect(host="ec2-54-247-118-238.eu-west-1.compute.amazonaws.com", dbname="d94l6q6a6g2mvm", user="jguojvyjehytsn", password="2fa3407deca1f2bc920fefc973912b3ed4388f727c6bd88039552d6032a458d9")
cur=bd.cursor()

def start(bot, up):
    up.message.reply_text('Hello (*・ω・)ﾉ')
    bot.sendDocument(chat_id=up.message.chat_id, document='CAADAQAD4AEAAkWQ0AeCTzUa7LnRbQI')
    check_id(up.message.chat.id)

def default(bot, up):
    if up.message.text!="Weight" and up.message.text!="Height" and up.message.text!="Age" and up.message.text!="EXIT":
        up.message.reply_text("Undefined ┐('～`;)┌")

def echo(bot, up):
    exit_admin(bot, up)
    button_1(bot, up)
    button_2(bot, up)
    button_3(bot, up)
    default(bot, up)

#___________________ID + BD Settings_____________________________________________________#

def check_id(id):                                                   # Пополнение базы data
    cur.execute("SELECT id from data;")
    data_id = cur.fetchall()
    if (id,) not in data_id:
        cur.execute("INSERT into data (id) VALUES({0});".format(id))
        bd.commit()

def db_add(number, param, id_db):
    cur.execute("UPDATE data SET {0} = {1} WHERE id = {2};".format(param, int(number), id_db))
    bd.commit()

#___________________Panel Settings_______________________________________________________#

keyb=[["Weight","Height", "Age"],["EXIT"]]
bot_panel=telegram.ReplyKeyboardMarkup(keyb,resize_keyboard=True,one_time_keyboard=True)
remove=telegram.ReplyKeyboardRemove()
force=telegram.ForceReply()

def parameters(bot, up):
    bot.sendMessage(up.message.chat.id,"Choose:",reply_markup=bot_panel)

#___________________Panel Processing_____________________________________________________#

def exit_admin(bot,up):
    if up.message.text=="EXIT": 
        bot.sendMessage(up.message.chat.id,"Exit (ノωヽ)",reply_markup=remove)

def button_1(bot,up):
    if up.message.text=="Weight": 
        bot.sendMessage(chat_id=up.message.chat.id, text="Enter your weight:", reply_markup=force) 
    if up.message.reply_to_message.text == "Enter your weight:":
        if(up.message.text>0):
                db_add(up.message.text, 'weight', up.message.chat.id)
                bot.sendMessage(up.message.chat.id, "Your weight is added. Check the table", reply_markup = remove)
        else:
                bot.sendMessage(chat_id=up.message.chat.id, text="Ooops, sorry, incorrect data. Try again!", reply_markup=remove)

def button_2(bot,up):
    if up.message.text=="Height":
        bot.sendMessage(up.message.chat.id,
                        "Enter your height:", reply_markup=force)

def button_3(bot, up):
    if up.message.text=="Age":
        bot.sendMessage(up.message.chat.id, "Enter your age (in months):", reply_markup=force)

#___________________Buttons Settings_____________________________________________________#

def get_callback_from_button(bot, up):
    query = up.callback_query
    username = up.effective_user.username
    chat_id = query.message.chat.id
    message_id = query.message.message_id
    if int(query.data) == 1:
        query.answer()
        api = '0f798fa08e77c5b4a2ad9d1bcbf5d700'
        try:
            settings = {'q': 'Tashkent', 'units': 'metric', 'lang': 'en', 'APPID': api}
            r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=settings)
            data = r.json()
            bot.sendMessage(
                chat_id=chat_id, text=f"Tomorrow's weather in Tashkent: {int(data['list'][1]['main']['temp_max'])}°C")
        except Exception as e:
            print("Exception (weather):", e)
            pass
    elif int(query.data) == 2:
        bot.sendMessage(chat_id=chat_id, text="You're welcome (^_~)")
        query.answer()

def buttons():
    keys = [[InlineKeyboardButton('Tomorrow', callback_data='1'), InlineKeyboardButton('No, thanks!', callback_data='2')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)



#___________________Tashkent Weather_____________________________________________________#

def weather(bot, up):
    api = '0f798fa08e77c5b4a2ad9d1bcbf5d700'
    try:
        settings = {'q': 'Tashkent', 'units': 'metric',
                    'lang': 'en', 'APPID': api}
        r = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast', params=settings)
        data = r.json()
        bot.sendMessage(chat_id=up.message.chat_id,
                        text=f"Current weather in Tashkent: {int(data['list'][0]['main']['temp_max'])}°C", reply_markup=buttons())
    except Exception as e:
        print("Exception (weather):", e)
        pass

#___________________dispatcher settgings_________________________________________________#

dp = up.dispatcher
start = CommandHandler("start", start)
parameters = CommandHandler("parameters", parameters)
weather = CommandHandler("weather", weather)
dp.add_handler(start)
dp.add_handler(parameters)
dp.add_handler(weather)
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(CallbackQueryHandler(get_callback_from_button))

#___________________webhook settings_____________________________________________________#

PORT = int(os.environ.get('PORT', '5000'))
TOKEN = "728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4"
up.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
up.bot.set_webhook("https://project-py-bot.herokuapp.com/728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")

up.idle()
