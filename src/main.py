#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
import logging
import json
from lib import stats, torrent

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)
MAGNET = range(1)
jsonFile = "/opt/raspibot-setup/raspibot/"
buttonTorrents = [InlineKeyboardButton(text="Add Torrent", callback_data="torrentAdd"), InlineKeyboardButton(text="Delete Torrent", callback_data="torrentDel"), InlineKeyboardButton(text="Torrent List", callback_data="torrentList")]
buttonMagnetCancel = [InlineKeyboardButton(text="<< Cancel", callback_data="magnetCancel")]

def build_menu(buttons,
			   n_cols: int):
	menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
	return menu

def start(bot, update):
	menuKeyboard = [["STATS"],["TORRENTS"]]
	update.message.reply_text(text="Hi, I'm your bitch", reply_markup=ReplyKeyboardMarkup(menuKeyboard))

def chatid(bot, update):
	update.message.reply_text(text=update.message.chat_id)

def getStats(bot, update):
	update.message.reply_text(text="<code>"+stats.stats()+"</code>", parse_mode="HTML")

def menuTorrents(bot, update):
	update.message.reply_text(text="Choose one option", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))

def addTorrent(bot, update):
	update.message.reply_text(text=torrent.addTorrent(update.message.text[12:]))

def button(bot, update):
	query = update.callback_query

	if query.data.startswith("del"):
		torrent.delTorrent(query.data[3:])
		query.message.edit_text(text="Torrente deleted", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))

	if query.data == "torrentList":
		query.message.edit_text(text="<code>"+str(torrent.getList(0))+"</code>", parse_mode="HTML", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))

	if query.data == "torrentDel":
		matrixTorrent=torrent.getList(1)
		listButtonTorrent = []
		for i in range(0, len(matrixTorrent)):
			listButtonTorrent.append(InlineKeyboardButton(text=matrixTorrent[i][1], callback_data="del"+str(matrixTorrent[i][0])))
		listButtonTorrent.append(InlineKeyboardButton(text="<< Back", callback_data="torrentBack"))
		query.message.edit_text(text="Choose one torrent to delete", reply_markup=InlineKeyboardMarkup(build_menu(listButtonTorrent, n_cols=1)))

	if query.data == "torrentAdd":
		query.message.reply_text(text="Paste the torrent's magnet")
		return MAGNET

	if query.data == "torrentBack":
		query.message.edit_text(text="Choose one option", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))

	if query.data == "magnetCancel":
		query.message.edit_text(text="Cancelled", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))
		return ConversationHandler.END

def response(bot, update):
	if (update.message.text=="STATS"):
		getStats(bot,update)
	if (update.message.text=="TORRENTS"):
		menuTorrents(bot,update)

def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def getMagnet(bot, update):
	if torrent.addTorrent(update.message.text)==0:
		update.message.reply_text(text="Magnet invalid. Try Again", reply_markup=InlineKeyboardMarkup(build_menu(buttonMagnetCancel, n_cols=2)))
		return MAGNET
	else:
		update.message.reply_text(text="Torrent added", reply_markup=InlineKeyboardMarkup(build_menu(buttonTorrents, n_cols=2)))
		return ConversationHandler.END

def cancel(bot, update):
    return ConversationHandler.END

def main():
	with open(jsonFile+'data.json') as json_data:
		d = json.load(json_data)
		updater = Updater(d["token"])

	dp = updater.dispatcher

	# Start
	dp.add_handler(CommandHandler("start", start))

	# ChatID
	dp.add_handler(CommandHandler("chatid", chatid))

	# Stats
	dp.add_handler(CommandHandler("stats", getStats))

	conv_handler = ConversationHandler(
		entry_points=[CallbackQueryHandler(button)],

		states={
			MAGNET: [MessageHandler(Filters.text, getMagnet)]
		},
		fallbacks=[CallbackQueryHandler(button)]
	)

	dp.add_handler(conv_handler)
	# Response
	dp.add_handler(MessageHandler(Filters.text, response))
	dp.add_handler(CallbackQueryHandler(button))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
