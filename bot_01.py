# python-telegram-bot
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

def getTextHTML(url):
	try:
		response = requests.get(url, timeout=(10, 10)).text

	except requests.exeptions.RequestExeption:
		response = 'ERROR'

	return response

def getExchangeRates(text):
	soup = BeautifulSoup(text, 'html.parser')
	blocks_list = soup.select('.tek-moment > .block')
	usd = blocks_list[0].find('a', class_='value').text
	usd = float(usd)
	eur = blocks_list[1].find('a', class_='value').text
	eur = float(eur)
	return {'USD': usd,
			'EUR': eur}

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

def getRates(bot,update):
	textHTML = getTextHTML('https://www.audit-it.ru/currency/')
	exchange_rates = getExchangeRates(textHTML)
	update.message.reply_text(
		'''Exchange rates:\nUSD = {0}\nEUR = {1}'''.format(
			exchange_rates['USD'],
			exchange_rates['EUR']))


f = open('bot_01_token.txt')
token = f.read()
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('gr', getRates))

updater.start_polling()
updater.idle()

# import pdb; pdb.set_trace()