#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RaspiBot

import telebot
from telebot import types
import cStringIO
import time
from lock.lock import *
from classrb.classrb import *
from functions.functions import *

rb=raspiBot
bot = telebot.TeleBot(rb.API_TOKEN)

#######################################################
#########       Comandos que escucha         ##########
#######################################################

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Hola, soy tu asistente personal")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text = message.text
    response = 'Elija una opcion'
    chat_id = message.chat.id
    key_v = False
    markup = types.ReplyKeyboardMarkup()

    if text == '/chatid':
        response = "Su ID es: "+str(chat_id)
    elif text == '/check':
        response = "ALL OK"
    if rb.ID == chat_id and rb.rssadd == False and rb.rssdel == False:
        if text.startswith('/rss'):
            if text == '/rss':
                markup = types.ReplyKeyboardMarkup()
                markup.row('/rss on','/rss off')
                markup.row('/rss add', '/rss del')
                markup.row('/rss status','/rss list')
                markup.row('/cancel')
                key_v = True
            else:
                response = modificar_rss(text[5:],rb)
        elif text.startswith('/google'):
            if(len(text)==7):
                response = "Existen dos sintaxis correctas, la primera tiene 5 resultados por defecto:\n"+"/google [busqueda]\n"+"/google -[num de resultados(1-8)] [busqueda]"
            else:
               response = funcion_google(text[7:])
        elif text.startswith('/img'):
            if(len(text)==4):
                response = "La sintaxis correcta es:\n"+"/img [busqueda]"
            else:
                funcion_img(text[4:],rb.ruta_img)
                img = open(rb.ruta_img+'/image.jpg', 'rb')
                bot.send_photo(chat_id, img)
                img.close()
        elif text.startswith('/wiki'):
            if(len(text)==5):
                response = "La sintaxis correcta es:\n"+"/wiki [busqueda]"
            else:
                response = funcion_wiki(text[6:])
        elif text.startswith('/ambilight'):
            if text == '/ambilight':
                markup = types.ReplyKeyboardMarkup()
                markup.row('/ambilight on')
                markup.row('/ambilight off')
                markup.row('/ambilight status')
                markup.row('/cancel')
                key_v = True
            else:
                response = modificar_ambilight(text[11:],rb)
        elif text.startswith('/torrent'):
            if text == '/torrent':
                markup = types.ReplyKeyboardMarkup()
                markup.row('/torrent on')
                markup.row('/torrent off')
                markup.row('/torrent status')
                markup.row('/cancel')
                key_v = True
            else:
                response = modificar_torrent(text[9:],rb)
        elif text == '/cancel':
            key_v = False
        elif text == '/help':
            response = "Comandos disponibles:\n"+"/chatid - Devuelve la ID del chat\n"+"/rss - Gestiona el servicio RSS\n"+"/ambilight - Gestiona el servicio ambilight\n"+"/torrent - Gestiona el servicio de aviso de torrents\n"+"/google - Realiza busquedas en google\n"+"/img - Realiza busquedas de imagenes en google\n"+"/wiki - Realiza busquedas en Wikipedia\n"
        sendWithKeyboard(response,markup,key_v)
    elif rb.rssadd == True or rb.rssdel == True:
        response = comprobar_rss(text,rb)
        sendWithKeyboard(response)
    else:
        response = "Comando no encontrado, use /help para informacion"


def sendWithKeyboard(response,markup=False,key=False):
    if markup == False:
        markup = types.ReplyKeyboardMarkup()
    if key == False:
        markup.row('/ambilight')
        markup.row('/rss')
        markup.row('/torrent')
        markup.row('/check')
    bot.send_message(rb.ID, text=response, reply_markup=markup)


#######################################################

setup_ini(rb)

bot.polling()

while True:
    time.sleep(1)
    if rb.torrent_v == True:
        mens_t=check_file(rb.filetorrent)
        if mens_t: sendWithKeyboard(mens_t)
    if rb.rss_v == True and rb.cont == 60:
        mens_rss=funcion_rss(rb)
        if mens_rss: sendWithKeyboard(mens_rss)
        rb.cont = 0
    rb.cont += 1
    pass
