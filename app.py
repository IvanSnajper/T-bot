import telebot
from config import *
from extentions import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты>  <в какую валюту перевести>\
<количество переводимой валюты>\nУвидеть список всех доступных валют можно командой: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты"
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        v = message.text.split()

        if len(v) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = v
        result = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f"Цена {amount} {quote} в {base} равна {result}"
        bot.send_message(message.chat.id, text)


bot.polling()