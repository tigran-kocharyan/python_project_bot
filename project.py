from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import requests, os, telegram, datetime
import psycopg2 as sql

up = Updater("728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
dp = up.dispatcher
bd = sql.connect(host="ec2-54-247-118-238.eu-west-1.compute.amazonaws.com", dbname="d94l6q6a6g2mvm", user="jguojvyjehytsn", password="2fa3407deca1f2bc920fefc973912b3ed4388f727c6bd88039552d6032a458d9")
cur= bd.cursor()

#___________________Commands Settings____________________________________________________#
def start(bot, up):
    bot.sendMessage(chat_id=up.message.chat.id, text="Hello. Bot works👌\nUse `/help` to get to know with functions this bot can perform", parse_mode=telegram.ParseMode.MARKDOWN)
    bot.sendDocument(chat_id=up.message.chat_id, document='CAADAQAD4AEAAkWQ0AeCTzUa7LnRbQI')
    check_id(up.message.chat.id)
def help(bot, up):
    bot.sendMessage(chat_id=up.message.chat.id, text="*Hey✌️ I am an assistant  bot 🤖*\nI can help you to monitor your health, show the weather and later will be able to remind you to do smth.\nJust text me your parameters for now.", parse_mode=telegram.ParseMode.MARKDOWN)
def echo(bot, up):
    button_check(bot, up)

#___________________ID + BD Settings_____________________________________________________#
def check_id(id):                                                   # Занесение ID в базу данных data
    cur.execute("SELECT id from data;")
    data_id = cur.fetchall()
    if (id,) not in data_id:
        cur.execute("INSERT into data (id) VALUES({0});".format(id))
        bd.commit()
def db_add(number, param, id_db):                                   # Занесение параметров пользователя в data
    cur.execute(f"UPDATE data SET {param} = {number} WHERE id = {id_db};")
    bd.commit()

#___________________Panel + Buttons Settings_____________________________________________#
remove=telegram.ReplyKeyboardRemove()
force=telegram.ForceReply()
med_keyb=[["Weight","Height", "Age"],["My Health"],["EXIT"]]                      # Med Settings
med_panel_set=telegram.ReplyKeyboardMarkup(med_keyb,resize_keyboard=True,one_time_keyboard=True)

def buttons():
    keys = [[InlineKeyboardButton('Tomorrow', callback_data='1'), InlineKeyboardButton('No, thanks!', callback_data='2')]]
    return InlineKeyboardMarkup(inline_keyboard=keys)
def med_panel(bot, up):
    bot.sendMessage(up.message.chat.id,"Choose:",reply_markup=med_panel_set)

#___________________Functions Processing_________________________________________________#
def body_surface_area(weight, height):
    body_surface_area_number = float(((weight*height)**(1/2))/60)
    return("{0:.10f}".format(body_surface_area_number))

def body_mass_index(weight, height):
    body_mass_index_number = float((weight*10000)/(height*height))
    return("{0:.10f}".format(body_mass_index_number))

def body_mass_index_spec(bmi):
    if bmi <= 16:
        return("Acute Underweight.")
    elif bmi > 16 and bmi <= 18.5:
        return("Underweight.")
    elif bmi > 18.5 and bmi <= 25:
        return("Standard.")
    elif bmi > 25 and bmi <= 30:
        return ("Overweight.")
    elif bmi > 30 and bmi <= 35:
        return("First Degree Obesity.")
    elif bmi > 35 and bmi <= 40:
        return("Second Degree Obesity.")
    elif bmi > 40:
        return("Third Degree Obesity.")

def get_health(id):
    cur.execute(f"SELECT * from data where id={id};")
    health_param = cur.fetchone()
    bsa=body_surface_area(float(health_param[3]), float(health_param[1])) #bsa=body_surface_area
    bmi=body_mass_index(float(health_param[3]), float(health_param[1])) #bmi=body_mass_index
    bmi_specification=body_mass_index_spec(float(bmi))
    message_text=f"*Your BSA = {bsa}\nYour BMI = {bmi} | {bmi_specification}*"
    return message_text

def get_weather(api):
    settings = {'q': 'Tashkent', 'units': 'metric', 'lang': 'en', 'APPID': api}
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast', params=settings)
    return(r.json())

def try_except(function):
    def wrapper(*args):
        try:
            function(*args)
        except:
            args[0].sendMessage(chat_id=args[1].message.chat.id, text="Ooops, sorry, incorrect data. Try again! ┐('～`;)┌", reply_markup=remove)
    return wrapper
#_________________________________________________________________________________________________#
@try_except
def button_check(bot, up): # Panel Processing
        if up.message.text=="EXIT":
            bot.sendMessage(up.message.chat.id,"Exit 😥",reply_markup=remove)

        elif up.message.text=="Weight": # Weight Processing
            bot.sendMessage(chat_id=up.message.chat.id, text="Enter your weight (use point with floating point numbers):", reply_markup=force)
        elif up.message.text=="Height": # Height Processing
            bot.sendMessage(chat_id=up.message.chat.id, text="Enter your height in integers:", reply_markup=force)
        elif up.message.text=="Age":    # Age Processing
            bot.sendMessage(chat_id=up.message.chat.id, text="Enter the number of years and months since your last birthday (use strictly this order with a space between them):", reply_markup=force)

        elif up.message.text=="My Health":
            health_text=get_health(up.message.chat.id)
            bot.sendMessage(chat_id=up.message.chat.id, text=health_text, parse_mode=telegram.ParseMode.MARKDOWN)
        elif up.message.reply_to_message.text == "Enter the number of years and months since your last birthday (use strictly this order with a space between them):": # Answer Processing
            years_months=up.message.text.split() #splitting the answer into separated words
            db_add((int(years_months[0]))*12+int(years_months[1]), 'age', up.message.chat.id)
            bot.sendMessage(up.message.chat.id, "Your age is added. Check the table!👌", reply_markup = remove)
        elif up.message.reply_to_message.text == "Enter your weight (use point with floating point numbers):" and (float(up.message.text))>=0:
            db_add(float(up.message.text), 'weight', up.message.chat.id)
            bot.sendMessage(up.message.chat.id, "Your weight is added. Check the table!👌", reply_markup = remove)
        elif up.message.reply_to_message.text == "Enter your height in integers:" and (int(up.message.text))>0:
            db_add(int(up.message.text), 'height', up.message.chat.id)
            bot.sendMessage(up.message.chat.id, "Your height is added. Check the table!👌", reply_markup = remove)

        else:
            bot.sendMessage(chat_id=up.message.chat.id, text="Ooops, sorry, incorrect data. Try again! ┐('～`;)┌", reply_markup=remove)

#_________________________________________________________________________________________________#
@try_except
def weather(bot, up): # Tashkent Weather
    data=get_weather('0f798fa08e77c5b4a2ad9d1bcbf5d700')
    bot.sendMessage(chat_id=up.message.chat_id, text=f"Current weather in Tashkent: {int(data['list'][0]['main']['temp_max'])}°C", reply_markup=buttons())

@try_except
def get_callback_from_button(bot, up): # Buttons Processing
    if int(up.callback_query.data) == 1:
        up.callback_query.answer()
        data = get_weather('0f798fa08e77c5b4a2ad9d1bcbf5d700')
        bot.sendMessage(chat_id=up.callback_query.message.chat.id, text=f"Tomorrow's weather in Tashkent: {int(data['list'][1]['main']['temp_max'])}°C")
    elif int(up.callback_query.data) == 2:
        up.callback_query.answer()
        bot.sendMessage(chat_id=up.callback_query.message.chat.id, text="You're welcome 🤗")

#___________________Dispatcher settgings_________________________________________________#
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("med_panel", med_panel))
dp.add_handler(CommandHandler("weather", weather))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(CallbackQueryHandler(get_callback_from_button))

#___________________webhook settings_____________________________________________________#
PORT = int(os.environ.get('PORT', '5000'))
TOKEN = "728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4"
up.start_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
up.bot.set_webhook("https://project-py-bot.herokuapp.com/728506589:AAEwkNES9a9koAm8CKaOqUDorarnRJaeFY4")
