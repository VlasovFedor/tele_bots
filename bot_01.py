# python-telegram-bot
import requests
import math
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

class BotHandler:

	def __init__(self):
		self.boundary = 0
		self.sales_rates = 1
		self.money = []

	def getTextHTML(self, url):
		try:
			response = requests.get(url, timeout=(10, 10)).text

		except requests.exeptions.RequestExeption:
			response = 'ERROR'

		return response

	def getExchangeRates(self, text):
		soup = BeautifulSoup(text, 'html.parser')
		blocks_list = soup.select('.tek-moment > .block')
		usd = blocks_list[0].find('a', class_='value').text
		usd = float(usd)
		eur = blocks_list[1].find('a', class_='value').text
		eur = float(eur)
		return {'USD': usd,
				'EUR': eur}

	def setBoundary(self, bot, update, args):
		self.boundary = float(args[0])
		update.message.reply_text('Boundary is set ' + str(self.boundary))

	def showBoundary(self, bot, update):
		update.message.reply_text('Boundary is ' + str(self.boundary))

	def addMoney(self, bot, update, args):
		self.money.append({'sum': float(args[0]),
				   'rate': float(args[1])})
		update.message.reply_text(
			'''Add {0} $ with rate {1}'''.format(
				args[0],
				args[1]))

	def showMyMoney(self, bot, update):
		textHTML = self.getTextHTML('https://www.audit-it.ru/currency/')
		exchange_rates = self.getExchangeRates(textHTML)
		usd = exchange_rates['USD'] - self.sales_rates
		sum_difference = 0
		for position in self.money:
			difference = (position['sum']*usd -
				position['sum']*position['rate'])
			update.message.reply_text(
				'''{0} $ was bougth with rate {1}\n
				Difference is {2}'''.format(
					position['sum'],
					position['rate'],
					difference))
			sum_difference += difference
		update.message.reply_text("Sum difference {}".format(
			sum_difference))

	def getRates(self, bot,update):
		textHTML = self.getTextHTML('https://www.audit-it.ru/currency/')
		exchange_rates = self.getExchangeRates(textHTML)
		update.message.reply_text(
			'''Exchange rates:\nUSD = {0}\nEUR = {1}'''.format(
				exchange_rates['USD'],
				exchange_rates['EUR']))
		if math.fabs(exchange_rates['USD'] - self.boundary) <= 0.5:
			text = '''USD boundary {} is reached'''.format(exchange_rates['USD'])
			update.message.reply_text(text)


	def callbackHour(self, bot, job):
		f = open('user_id.txt')
		chat_id = f.read()
		f.close()
		textHTML = self.getTextHTML('https://www.audit-it.ru/currency/')
		exchange_rates = self.getExchangeRates(textHTML)
		text = '''Exchange rates:\nUSD = {0}\nEUR = {1}'''.format(
				exchange_rates['USD'],
				exchange_rates['EUR'])
		bot.send_message(chat_id=chat_id,
						 text=text)
		usd = exchange_rates['USD']
		if math.fabs(usd - self.boundary) <= 0.5:
			text = '''USD boundary {} is reached'''.format(usd)
			bot.send_message(chat_id=chat_id,
							 text=text)


bot_handler = BotHandler()
f = open('bot_01_token.txt')
token = f.read()
f.close()

updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('sb',
									bot_handler.setBoundary,
									pass_args=True))
updater.dispatcher.add_handler(CommandHandler('gr',
									bot_handler.getRates))
updater.dispatcher.add_handler(CommandHandler('am',
									bot_handler.addMoney,
									pass_args=True))
updater.dispatcher.add_handler(CommandHandler('smm',
									bot_handler.showMyMoney))
updater.dispatcher.add_handler(CommandHandler('shb',
									bot_handler.showBoundary))

job_queue = updater.job_queue

job_hour = job_queue.run_repeating(bot_handler.callbackHour,
									 interval = 10800,
									 first = 0)

updater.start_polling()
updater.idle()
