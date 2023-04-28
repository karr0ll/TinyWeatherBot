from constants import TOKEN

import telebot

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.reply_to(message, "привет")


if __name__ == "__main__":
    bot.infinity_polling()