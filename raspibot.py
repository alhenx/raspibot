#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RaspiBot

import telebot
from telebot import types
import random
import urllib
import json
import cStringIO
import os
import time
import feedparser
import wikipedia

ambi_v = False
rss_v = False
torrent_v = False
cont = 0
listaurls=[]
listarss=[]
bdrss=[]

#######################################################
#########          ZONA MODIFICABLE          ##########
#######################################################

#TOKEN del bot
API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

#Identificador del chat
chat_id =

#Ruta del bot
ruta=''

#Ruta del ambilight
ruta_ambi=''

#Ruta para el torrent
filetorrent = ""

#Lista de feeds para el RSS
listaurls.append('http://feeds.feedburner.com/linuxenandalu?format=xml')



#######################################################




#######################################################
#########       Comandos que escucha         ##########
#######################################################

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text=message.text
    chat_id=message.chat.id
    key_v = False
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)

    if text == '/prueba':
        bot.send_message(chat_id, text="Funsiono y tu id es: "+str(chat_id))
    elif text.startswith('/rss'):
        if text == '/rss':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('/rss on')
            markup.row('/rss off')
            markup.row('/rss status')
            markup.row('/cancel')
            key_v = True
        else:
            modificar_rss(text[5:])
    elif text.startswith('/google'):
        if(len(text)==7):
            bot.send_message(chat_id, text="Existen dos sintaxis correctas, la primera tiene 5 resultados por defecto:\n"+
            "/google [busqueda]\n"+
            "/google -[num de resultados(1-8)] [busqueda]")
        else:
           funcion_google(text[7:])
    elif text.startswith('/img'):
        if(len(text)==4):
            bot.send_message(chat_id, text="La sintaxis correcta es:\n"+
            "/img [busqueda]")
        else:
            funcion_img(text[4:])
    elif text.startswith('/wiki'):
        if(len(text)==5):
            bot.send_message(chat_id, text="La sintaxis correcta es:\n"+
            "/wiki [busqueda]")
        else:
           funcion_wiki(text[6:])
    elif text.startswith('/ambilight'):
        if text == '/ambilight':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('/ambilight on')
            markup.row('/ambilight off')
            markup.row('/ambilight status')
            markup.row('/cancel')
            key_v = True
        else:
            modificar_ambilight(text[11:])
    elif text.startswith('/torrent'):
        if text == '/torrent':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row('/torrent on')
            markup.row('/torrent off')
            markup.row('/torrent status')
            markup.row('/cancel')
            key_v = True
        else:
            modificar_torrent(text[9:])
    elif text == '/cancel':
        key_v = False
    if key_v == False:
        markup.row('/ambilight')
        markup.row('/rss')
        markup.row('/torrent')
    bot.send_message(chat_id, 'Seleccione un comando', reply_markup=markup)

#######################################################

#######################################################
#########        Funciones principales       ##########
#######################################################

def modificar_torrent(text):
    global torrent_v,ruta
    if text == 'on':
        torrent_v = True
        cmd = '> '+ruta+'/lock/torrent'
        os.system(cmd)
        bot.send_message(chat_id, text="Aviso de torrent activado")
    if text == 'off':
        torrent_v = False
        cmd = 'rm '+ruta+'/lock/torrent'
        os.system(cmd)
        bot.send_message(chat_id, text="Aviso de torrent desactivado")
    if text == 'status':
        if torrent_v == True:
            bot.send_message(chat_id, text="El aviso de torrent esta activado")
        else:
            bot.send_message(chat_id, text="El aviso de torrent esta desactivado")

def modificar_ambilight(text):
    global ambi_v,ruta
    if text == 'on':
        ambi_v = True
        cmd = '> '+ruta+'/lock/ambilight'
        os.system(cmd)
        cmd = ruta_ambi+' -o saturation=2.0 -p 100 -f /dev/null > /dev/null'
        os.system(cmd)
        bot.send_message(chat_id, text="Ambilight activado")
    if text == 'off':
        ambi_v = False
        cmd = 'rm '+ruta+'/lock/ambilight'
        os.system(cmd)
        pid = os.popen('pidof boblight-dispmanx').read()
        cmd ='kill -9 '+pid
        os.system(cmd)
        bot.send_message(chat_id, text="Ambilight desactivado")
    if text == 'status':
        if ambi_v == True:
            bot.send_message(chat_id, text="Ambilight esta activado")
        else:
            bot.send_message(chat_id, text="Ambilight esta desactivado")

def modificar_rss(text):
    global rss_v,ruta
    if text == 'on':
        rss_v = True
        cmd = '> '+ruta+'/lock/rss'
        os.system(cmd)
        bot.send_message(chat_id, text="RSS activado")
    if text == 'off':
        rss_v = False
        cmd = 'rm '+ruta+'/lock/rss'
        os.system(cmd)
        bot.send_message(chat_id, text="RSS desactivado")
    if text == 'status':
        if rss_v == True:
            bot.send_message(chat_id, text="RSS esta activado")
        else:
            bot.send_message(chat_id, text="RSS esta desactivado")

def funcion_rss():
    global listarss
    global bdrss
    del listarss[:]
    for i in range(0,len(listaurls)):
        listarss.append(feedparser.parse(listaurls[i]))
    for i in range(0,len(listarss)):
        if listarss[i].entries[0].title not in bdrss:
            bot.send_message(chat_id, text="Noticia nueva:\n"+ listarss[i].entries[0].title + ": \n"+ listarss[i].entries[0].link + "\n")
            bdrss.append(listarss[i].entries[0].title)


def funcion_google(text):
    if(text[0] == '-'):
        num = text[1]
    else:
        num = 5
        lista = ''
        query = text.encode('utf-8')
        query = urllib.urlencode ( { 'q' : query } )
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=%s&%s' % (num,query)
        search_response = urllib.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results)
        data = results[ 'responseData' ]
        hits = data['results']
        for h in hits: lista+=(h['url']+'\n')
        bot.send_message(chat_id, text=lista)

def funcion_img(text):
    global ruta
    lista = []
    query = text.encode('utf-8')
    query = urllib.urlencode ( { 'q' : query } )
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&rsz=8&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results[ 'responseData' ]
    hits = data['results']
    for h in hits: lista.append(h['url'])
    f = open(ruta+'/img/image.jpg','wb')
    f.write(urllib.urlopen(random.choice(lista)).read())
    f.close()
    img = open(ruta+'/img/image.jpg', 'rb')
    bot.send_photo(chat_id, img)
    img.close()

def funcion_wiki(text):
    wikipedia.set_lang("es")
    bot.send_message(chat_id, text=wikipedia.page(text).url)

#######################################################

#######################################################
#########           Funciones lock           ##########
#######################################################

def lock_torrent():
    global torrent_v,ruta
    file = ruta+"/lock/torrent"
    fileexists = os.path.isfile(file)
    if fileexists:
        torrent_v = True
    else:
        torrent_v = False

def lock_rss():
    global rss_v,ruta
    file = ruta+"/lock/rss"
    fileexists = os.path.isfile(file)
    if fileexists:
        rss_v = True
    else:
        rss_v = False

def lock_ambi():
    global ambi_v,ruta
    file = ruta+"/lock/ambilight"
    fileexists = os.path.isfile(file)
    if fileexists:
        ambi_v = True
        cmd = '> '+ruta+'/lock/ambilight'
        os.system(cmd)
        cmd = ruta_ambi+' -o saturation=2.0 -p 100 -f /dev/null > /dev/null'
        os.system(cmd)
    else:
        ambi_v = False
        cmd = 'rm '+ruta+'/lock/ambilight'
        os.system(cmd)
        pid = os.popen('pidof boblight-dispmanx').read()
        cmd ='kill -9 '+pid
        os.system(cmd)

#######################################################



#######################################################
#########          Funciones Torrent         ##########
#######################################################

def check_file():
  if isfile(filetorrent):
    wcout = count_filelines(filetorrent)
    if wcout > 1:
      bot.send_message(chat_id, text="Torrents completados:\n"+cat_file(filetorrent))
    else :
      bot.send_message(chat_id, text="Torrents completado:\n"+cat_file(filetorrent))
    newwcout = count_filelines(filetorrent)
    if wcout < newwcout :
    #Si se han añadido más lineas desde la ultima vez
        check_file()
    rm_file(filetorrent)

def rm_file(rmfile):
    if isfile(rmfile):
        rm = "rm "+rmfile+" > /dev/null 2>&1"
        os.system(rm)

def count_filelines(wcfile):
    wc = "cat "+wcfile+" | wc -l"
    return int(os.popen(wc).read())

def cat_file(catfile):
    cat = "cat "+catfile
    return os.popen(cat).read()

def isfile(fileexists):
    return os.path.isfile(fileexists)

#######################################################


#######################################################
#########   Comprobaciones previas al iniciar  ########
#######################################################

for i in range(0,len(listaurls)):
    listarss.append(feedparser.parse(listaurls[i]))
for i in range(0,len(listarss)):
        bdrss.append(listarss[i].entries[0].title)


lock_rss()
lock_ambi()
lock_torrent()

bot.polling()
#######################################################

while True:
    time.sleep(1)
    if torrent_v == True:
        check_file()
    if rss_v == True and cont == 60:
        funcion_rss()
        cont = 0
    cont += 1
    pass
