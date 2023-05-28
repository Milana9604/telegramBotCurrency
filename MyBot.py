import telebot
import requests
import json

TOKEN = "6102205535:AAH9aDe9Ww8yDn0jSgOMlfNbf7qepSz8j6w"
bot = telebot.TeleBot(TOKEN)

keys = {
    "рубль" : "RUB",
    "доллар" : "USD",
    "евро" : "EUR"
}

class ConvertionExeptuon(Exception):
    pass

class Converter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

            if quote == base:
                raise ConvertionExeptuon(f'Невозможно перевести одинаковые валюты {base}.')

            try:
                quote_ticker = keys[quote]
            except KeyError:
                raise ConvertionExeptuon(f'Не удалось обработать валюту {quote}.')

            try:
                base_ticker = keys[base]
            except KeyError:
                raise ConvertionExeptuon(f'Не удалось обработать валюту {base}.')

            try:
                amount = float(amount)
            except ValueErrorError:
                raise ConvertionExeptuon(f'Не удалось обработать количество {amount}.')

            r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
            total_base = json.loads(r.content)[base_ticker]

            return total_base

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в следующем порядке: \n<имя валюты> <в какую валюту перевести> \ ' \
     '<количество переводимой валюты>\
    \n Увидеть список доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    bot.reply_to(message, text)
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    quote, base, amount = values

    if len(values) != 3:
        raise ConvertionExeptuon('Слишком много параметров.')

    total_base = Converter.convert(quote, base, amount) * float(amount)
    text = f'{amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()