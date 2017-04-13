#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

jsonFile = "/opt/raspibot/"

def chatid(bot, update):
	update.message.reply_text(quote=True, text=update.message.chat_id)

def response(bot, update):
	if (update.message.text=="token"):
		with open(jsonFile+'data.json') as json_data:
			d = json.load(json_data)
		update.message.reply_text(quote=True, text=d["token"])

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	with open(jsonFile+'data.json') as json_data:
		d = json.load(json_data)
		updater = Updater(d["token"])

	dp = updater.dispatcher

	# ChatID
	dp.add_handler(CommandHandler("chatid", chatid))

	# Response
	dp.add_handler(MessageHandler(Filters.text, response))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
