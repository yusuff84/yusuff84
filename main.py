import telebot
import config
import time
import requests

globalusd = 0

bot = telebot.TeleBot(config.TOKEN)


def percent(endNum, firstNum):
    return round(((float(firstNum) * 100 / float(endNum)) - 100), 2)


def pars():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)
    btcToUsd = response.json()['price']
    return float(btcToUsd)


# print(pars())
# print(percent(pars(),globalusd))


@bot.message_handler(commands=['start'])
def startBot(message, ):
    bot.send_message(message.chat.id, "Курс Bitcoin " + str(pars()) + "$")
    globalusd = pars()
    while True:
        if percent(globalusd, pars()) >= 1:
            globalusd = pars()
            bot.send_message(message.chat.id, "Курс Биткоина Вырос на +" + (
                        str(percent(globalusd, pars())) + "%" + "\nСейчас 1В-" + str(pars())) + "$")
        elif percent(globalusd, pars()) <= -1:
            globalusd = pars()
            bot.send_message(message.chat.id, "Курс Биткоина Упал на " + (
                        str(percent(globalusd, pars())) + "%" + "\nСейчас 1В-" + str(pars())) + "$")
        time.sleep(60)


@bot.message_handler(content_types=['text'])
def TextChat(message):
    if "биткоин" or "bitcoin" in message.text.lower():
        bot.send_message(message.chat.id, "Курс Bitcoin " + str(pars()) + "$")


bot.polling(none_stop=True)
