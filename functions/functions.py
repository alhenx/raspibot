#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import feedparser
import urllib
import json
import random
import wikipedia

#######################################################
#########        Funciones principales       ##########
#######################################################

def modificar_torrent(text,rb):
    if text == 'on':
        rb.torrent_v = True
        cmd = '> '+rb.ruta_tmp+'/torrent'
        os.system(cmd)
        return "Aviso de torrent activado"
    if text == 'off':
        rb.torrent_v = False
        cmd = 'rm '+rb.ruta_tmp+'/torrent'
        os.system(cmd)
        return "Aviso de torrent desactivado"
    if text == 'status':
        if rb.torrent_v == True:
            return "El aviso de torrent esta activado"
        else:
            return "El aviso de torrent esta desactivado"

def modificar_ambilight(text,rb):
    if text == 'on':
        rb.ambi_v = True
        cmd = '> '+rb.ruta_tmp+'/ambilight'
        os.system(cmd)
        cmd = rb.ruta_ambi+' -o saturation=2.0 -p 100 -f /dev/null > /dev/null'
        os.system(cmd)
        return "Ambilight activado"
    if text == 'off':
        rb.ambi_v = False
        cmd = 'rm '+rb.ruta_tmp+'/ambilight'
        os.system(cmd)
        pid = os.popen('pidof boblight-dispmanx').read()
        cmd ='kill -9 '+pid
        os.system(cmd)
        return "Ambilight desactivado"
    if text == 'status':
        if rb.ambi_v == True:
            return "Ambilight esta activado"
        else:
            return "Ambilight esta desactivado"

def modificar_rss(text,rb):
    if text == 'on':
        rb.rss_v = True
        cmd = '> '+rb.ruta_tmp+'/rss'
        os.system(cmd)
        return "RSS activado"
    if text == 'off':
        rb.rss_v = False
        cmd = 'rm '+rb.ruta_tmp+'/rss'
        os.system(cmd)
        return "RSS desactivado"
    if text == 'status':
        if rb.rss_v == True:
            return "RSS esta activado"
        else:
            return "RSS esta desactivado"

def funcion_rss(rb):
    del rb.listarss[:]
    for i in range(0,len(rb.listaurls)):
        rb.listarss.append(feedparser.parse(rb.listaurls[i]))
    for i in range(0,len(rb.listarss)):
        if rb.listarss[i].entries[0].title not in rb.bdrss:
            rb.bdrss.append(rb.listarss[i].entries[0].title)
            return "Noticia nueva:\n"+ rb.listarss[i].entries[0].title + ": \n"+ rb.listarss[i].entries[0].link


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
        return lista

def funcion_img(text,ruta_img):
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
    f = open(ruta_img+'/image.jpg','wb')
    f.write(urllib.urlopen(random.choice(lista)).read())
    f.close()

def funcion_wiki(text):
    wikipedia.set_lang("es")
    return wikipedia.page(text).url

#######################################################


#######################################################
#########          Funciones Torrent         ##########
#######################################################

def check_file(filetorrent):
  if isfile(filetorrent):
    wcout = count_filelines(filetorrent)
    if wcout > 1:
      message="Torrents completados:\n"+cat_file(filetorrent)
    else :
      message="Torrents completado:\n"+cat_file(filetorrent)
    newwcout = count_filelines(filetorrent)
    if wcout < newwcout :
    #Si se han añadido más lineas desde la ultima vez
        check_file()
    rm_file(filetorrent)
    return message

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