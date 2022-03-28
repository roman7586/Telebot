import telebot
from telebot import types
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/Валюты")
    btn2 = types.KeyboardButton("/Инструкция")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, text="Привет! Я тестовый бот для для конвертации валют. Выберите команду для\
получения помощи ниже, либо если известен алгоритм работы бота укажите конвертируемые валюты \
в соответсвии с правилами".format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['Инструкция'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите, команду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> <количество переводимой валюты>. Валюты указываются с маленькой буквы'
    bot.reply_to(message, text)

@bot.message_handler(commands=['Валюты'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:

        values = message.text.split(' ')

        if len(values) > 3:
            raise ConvertionException('Параметров для выполнения операций перевода более 3. \
            Воспользуйтесь инструкцией для понимания формата вводимых комманд')
        elif len(values) < 3:
            raise ConvertionException('Параметров для выполнения операций перевода менее 3. \
            Воспользуйтесь инструкцией для понимания формата вводимых комманд')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Допущена ошибка со стороны пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()

