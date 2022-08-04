import telebot
from telebot import types
import config
import random
from buttons import *

current_category = ""

games1_kb = types.ReplyKeyboardMarkup()
games1_kb.add(types.KeyboardButton('Далее ➡️'))
games2_kb = types.ReplyKeyboardMarkup()
games2_kb.add(types.KeyboardButton('⬅️ Назад'))
main_kb = types.ReplyKeyboardMarkup()

for btn in buttons_main:
  main_kb.add(types.KeyboardButton(btn))

i = 0
for btn in buttons_games:
  if i < 5:
    games1_kb.add(types.KeyboardButton(btn))
  elif i < 10:
    games2_kb.add(types.KeyboardButton(btn))
  i += 1

ages_kb = types.ReplyKeyboardMarkup()
for btn in buttons_ages:
  ages_kb.add(types.KeyboardButton(btn))

ages_kb2 = types.ReplyKeyboardMarkup()
for btn in mk_ages:
  ages_kb2.add(types.KeyboardButton(btn))

bot = telebot.TeleBot("5341343934:AAFIXHc4WxFtxQoTpacc26cQPvQi4407EYw")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.send_message(message.chat.id, "Я DRIVE BOT! Я помогу тебе найти нужную игру для детей, выберете категорию игры!", reply_markup=main_kb)

def send_game(message):
  game_path = ""
  number_of_games = 0
  if current_category in buttons_games:
    number_of_games = buttons_games[current_category][2][buttons_ages[message.text]]
  if number_of_games == 0:
    bot.send_message(message.chat.id, "Извините, игры этой категории пока не добавлены 😒", reply_markup=games1_kb)
  else:
    if current_category in buttons_games:
      game_path = buttons_games[current_category][1] + "/" + buttons_games[current_category][1] + buttons_ages[message.text] + str(random.randint(1,number_of_games))
    try:
      bot.send_photo(message.chat.id, photo=open(game_path + ".png", 'rb'))
    finally:
      bot.send_message(message.chat.id, "Что хотите посмотреть ещё?", reply_markup=main_kb)

def send_mk(message):
  game_path = ""
  if message.text == "Младшие":
    game_path = "MKM/MKM (" + str(random.randint(1,17)) + ").pdf"
  if message.text == "Старшие":
    game_path = "MKS/MKS (" + str(random.randint(1,4)) + ").pdf"
  with open(game_path, "rb") as file:
    bot.send_document(message.chat.id, document=file)
    bot.send_message(message.chat.id, "Что хотите посмотреть ещё?", reply_markup=main_kb)
    
@bot.message_handler(func=lambda message: True)
def echo_all(message):
  global current_category
  if message.text == "Игры 🎲":
    bot.send_message(message.chat.id, buttons_main[message.text], reply_markup=games1_kb)
  if message.text == "Мастер-классы 📜":
    bot.send_message(message.chat.id, buttons_main[message.text], reply_markup=ages_kb2)
  if message.text in buttons_games and message.text != "Далее ➡️" and message.text != "⬅️ Назад":
    bot.send_message(message.chat.id, buttons_games[message.text][0])
    bot.send_message(message.chat.id, "Выберете возраст детей для которых нужна игра", reply_markup=ages_kb)
    current_category = message.text
  if message.text in buttons_ages:
    send_game(message)
  if message.text in mk_ages:
    send_mk(message)
  if message.text == "Далее ➡️":
    bot.send_message(message.chat.id, "Хорошо, у нас ещё такие категории есть", reply_markup=games2_kb)
  if message.text == "⬅️ Назад":
    bot.send_message(message.chat.id, "Назад, так назад", reply_markup=games1_kb)
    
bot.infinity_polling()