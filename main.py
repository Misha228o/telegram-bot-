import telebot
import telebot
from extensions import APIException, CurrencyConverter
import config

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = ('Привет! Чтобы узнать стоимость валюты, отправьте сообщение в формате:\n'
            '<имя валюты, цену которой хотите узнать> <имя валюты, в которой узнать цену> <количество>\n'
            'Например:\nевро доллар 10\n\n'
            'Доступные команды:\n/values - список доступных валют')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:\n' + '\n'.join(CurrencyConverter.currencies.keys())
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException('Неверное количество параметров.')

        base, quote, amount = parts
        total = CurrencyConverter.get_price(base, quote, amount)
        text = f'{amount} {base} = {total} {quote}'
        bot.send_message(message.chat.id, text)

    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')
    except Exception:
        bot.send_message(message.chat.id, 'Неизвестная ошибка. Проверьте корректность ввода.')


bot.polling(none_stop=True)
