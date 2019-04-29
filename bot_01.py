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

def callback_hour(bot, job):
	f = open('user_id.txt')
	chat_id = f.read()
	f.close()
	textHTML = getTextHTML('https://www.audit-it.ru/currency/')
	exchange_rates = getExchangeRates(textHTML)
	text = '''Exchange rates:\nUSD = {0}\nEUR = {1}'''.format(
			exchange_rates['USD'],
			exchange_rates['EUR'])
	bot.send_message(chat_id=chat_id,
					 text=text)

f = open('bot_01_token.txt')
token = f.read()
f.close()

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('gr', getRates))
# updater.dispatcher.add_handler(CommandHandler(''))

job_queue = updater.job_queue

job_hour = job_queue.run_repeating(callback_hour,
									 interval = 3600,
									 first = 0)
updater.start_polling()
updater.idle()
