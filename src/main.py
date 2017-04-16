#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import json
import os
from lib import stats, torrent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

jsonFile = "/opt/raspibot-setup/raspibot/"

def build_menu(buttons,
               n_cols: int):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    return menu

def chatid(bot, update):
	update.message.reply_text(quote=True, text=update.message.chat_id)

def getStats(bot, update):
	update.message.reply_text(quote=True, text="<code>"+stats.stats()+"</code>", parse_mode="HTML")

def getTorrentList(bot, update):
	update.message.reply_text(quote=True, text="<code>"+str(torrent.getList(0))+"</code>", parse_mode="HTML")

def addTorrent(bot, update):
	update.message.reply_text(quote=True, text=torrent.addTorrent(update.message.text[12:]))
	
def delTorrent(bot, update):
	matrixTorrent=torrent.getList(1)
	button_list = []
	for i in range(0, len(matrixTorrent)):
		button_list.append(InlineKeyboardButton(text=matrixTorrent[i][1], callback_data="del"+str(matrixTorrent[i][0])))
	update.message.reply_text(quote=True, text="TESTING DELETE TORRENT", reply_markup=InlineKeyboardMarkup(build_menu(button_list, n_cols=1)))

def button(bot, update):
	query = update.callback_query

	if query.data.startswith("del"):
		torrent.delTorrent(query.data[3:])
		bot.editMessageText(text="Torrente deleted",
							chat_id=query.message.chat_id,
							message_id=query.message.message_id,)

def response(bot, update):
	if (update.message.text=="hola"):
		update.message.reply_text(quote=True, text="adios")

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
	with open(jsonFile+'/data.json') as json_data:
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
	dp.add_handler(CallbackQueryHandler(button))


	# Response
	dp.add_handler(MessageHandler(Filters.text, response))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
