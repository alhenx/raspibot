#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RaspiBot

import telebot
from telebot import types
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

    if rb.ID == chat_id:
        if text == 'CANCEL':
            rb.rss_m = False
            rb.ambi_m = False
            rb.torrent_m = False
            key_v = False
        elif rb.torrent_m == False and rb.rss_m == False and rb.ambi_m == False:
            if text.startswith('/google'):
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
            elif text == 'RSS':
                markup = types.ReplyKeyboardMarkup()
                markup.row('ON','OFF')
                markup.row('ADD', 'DEL')
                markup.row('STATUS','LIST')
                markup.row('CANCEL')
                rb.rss_m = True
                key_v = True
            elif text == 'AMBILIGHT':
                markup = types.ReplyKeyboardMarkup()
                markup.row('ON')
                markup.row('OFF')
                markup.row('STATUS')
                markup.row('CANCEL')
                rb.ambi_m = True
                key_v = True
            elif text == 'TORRENT':
                markup = types.ReplyKeyboardMarkup()
                markup.row('ALERT ON','ALERT OFF')
                markup.row('ADD', 'DEL')
                markup.row('ALERT STATUS','LIST')
                markup.row('CANCEL')
                rb.torrent_m = True
                key_v = True
            elif text == 'VERSION':
                url = "https://raw.githubusercontent.com/alhenx/raspibot/master/version"
                data = urllib.request.urlopen(url)
                data = data.read().decode("UTF-8")
                response ="Current Version: "+str(data)
            elif text == 'HELP':
                response = "Comandos disponibles:\n"+"RSS - Gestiona el servicio RSS\n"+"AMBILIGHT - Gestiona el servicio ambilight\n"+"TORRENT - Gestiona el servicio de aviso de torrents\n"+"/google - Realiza busquedas en google\n"+"/img - Realiza busquedas de imagenes en google\n"+"/wiki - Realiza busquedas en Wikipedia\n"+"VERSION - Comprueba la version del bot\n"
            else:
                response = "Comando no encontrado, use HELP para informacion"
        elif rb.torrent_m == True:
            markup = types.ReplyKeyboardMarkup()
            markup.row('ALERT ON','ALERT OFF')
            markup.row('ADD', 'DEL')
            markup.row('ALERT STATUS','LIST')
            markup.row('CANCEL')
            key_v = True
            response = modificar_torrent(text,rb)
        elif rb.ambi_m == True:
            markup = types.ReplyKeyboardMarkup()
            markup.row('ON')
            markup.row('OFF')
            markup.row('STATUS')
            markup.row('CANCEL')
            key_v = True
            response = modificar_ambilight(text,rb)
        elif rb.rss_m == True and rb.rssadd == False and rb.rssdel == False:
            markup = types.ReplyKeyboardMarkup()
            markup.row('ON','OFF')
            markup.row('ADD', 'DEL')
            markup.row('STATUS','LIST')
            markup.row('CANCEL')
            key_v = True
            response = modificar_rss(text,rb)
        elif rb.rssadd == True or rb.rssdel == True:
            markup = types.ReplyKeyboardMarkup()
            markup.row('ON','OFF')
            markup.row('ADD', 'DEL')
            markup.row('STATUS','LIST')
            markup.row('CANCEL')
            key_v = True
            if text == 'LIST':
                response = modificar_rss(text,rb)
                response +='\n Introduzca la opcion que desee'
            else:
                response = comprobar_rss(text,rb)
        sendWithKeyboard(response,markup,key_v)
    else:
        response = "Comando no encontrado, use HELP para informacion"


def sendWithKeyboard(response,markup=False,key=False):
    if markup == False:
        markup = types.ReplyKeyboardMarkup()
    if key == False:
        markup.row('TORRENT')
        markup.row('RSS')
        markup.row('AMBILIGHT')
        markup.row('VERSION', 'HELP')
    bot.send_message(rb.ID, text=response, reply_markup=markup)


#######################################################

setup_ini(rb)
if comprobar_update(rb) == True:
    version = open(rb.ruta_bot+'/version')
    version = version.read()
    sendWithKeyboard('Version actualizada ['+version+']')
if comprobar_version(rb) == False:
    sendWithKeyboard('Hay una nueva version disponible. Utilice "raspibot update" en su terminal.')
bot.polling(True)

while True:
    time.sleep(1)
    if rb.torrent_v == True:
        mens_t=check_file(rb.filetorrent)
        if mens_t: sendWithKeyboard(mens_t)
    if rb.rss_v == True and rb.cont == 60:
        mens_rss=funcion_rss(rb)
        if mens_rss: sendWithKeyboard(mens_rss)
        rb.cont = 0
    if comprobar_version(rb) == False and rb.contv == 3600:
        rb.contv = 0
        sendWithKeyboard('Hay una nueva version disponible. Utilice "raspibot update" en su terminal.')
    rb.cont += 1
    rb.contv += 1
    pass
