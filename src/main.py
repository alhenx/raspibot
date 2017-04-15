#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
from lib import stats, torrent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

jsonFile = "/opt/raspibot-setup/raspibot/"

def chatid(bot, update):
	update.message.reply_text(quote=True, text=update.message.chat_id)

def getStats(bot, update):
	update.message.reply_text(quote=True, text="<code>"+stats.stats()+"</code>", parse_mode="HTML")

def getTorrentList(bot, update):
	update.message.reply_text(quote=True, text="<code>"+torrent.getList()+"</code>", parse_mode="HTML")

def addTorrent(bot, update):
	update.message.reply_text(quote=True, text=torrent.addTorrent(update.message.text[12:]))

def delTorrent(bot, update):
	update.message.reply_text(quote=True, text=torrent.delTorrent(update.message.text[12:]))

def response(bot, update):
	if (update.message.text=="hola"):
		update.message.reply_text(quote=True, text="adios")

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	with open(jsonFile+'data.json') as json_data:
		d = json.load(json_data)
		updater = Updater(d["token"])

	dp = updater.dispatcher

	# ChatID
	dp.add_handler(CommandHandler("chatid", chatid))

	# Stats
	dp.add_handler(CommandHandler("stats", getStats))

	# Torrents
	dp.add_handler(CommandHandler("torrentlist", getTorrentList))
	dp.add_handler(CommandHandler("torrentadd", addTorrent))
	dp.add_handler(CommandHandler("torrentdel", delTorrent))

	# Response
	dp.add_handler(MessageHandler(Filters.text, response))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
