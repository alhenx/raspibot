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

def comprobar_update(rb):
    file = rb.ruta_tmp+"/update"
    fileexists = os.path.isfile(file)
    if fileexists:
        cmd = 'rm '+rb.ruta_tmp+'/update'
        os.system(cmd)
        return True
    else:
        return False

def comprobar_version(rb):
    try:
        url = "https://raw.githubusercontent.com/alhenx/raspibot/master/version"
        data = urllib.request.urlopen(url)
        data = data.read().decode("UTF-8")
        version = open(rb.ruta_bot+'/version')
        version = version.read()
        if str(data) != version:
            return False
        else:
            return True
    except:
        return True

def modificar_torrent(text,rb):
    if text == 'ALERT ON':
        rb.torrent_v = True
        cmd = '> '+rb.ruta_tmp+'/torrent'
        os.system(cmd)
        return "Aviso de torrent activado"
    if text == 'ALERT OFF':
        rb.torrent_v = False
        cmd = 'rm '+rb.ruta_tmp+'/torrent'
        os.system(cmd)
        return "Aviso de torrent desactivado"
    if text == 'ALERT STATUS':
        if rb.torrent_v == True:
            return "El aviso de torrent esta activado"
        else:
            return "El aviso de torrent esta desactivado"

def modificar_ambilight(text,rb):
    if text == 'ON':
        if rb.ruta_ambi != "NOPE":
            rb.ambi_v = True
            cmd = '> '+rb.ruta_tmp+'/ambilight'
            os.system(cmd)
            cmd = rb.ruta_ambi+' -p 100 -f /dev/null > /dev/null'
            os.system(cmd)
            return "Ambilight activado"
        else:
            return "No dispone de sistema ambilight"
    if text == 'OFF':
        if rb.ruta_ambi != "NOPE":
            rb.ambi_v = False
            cmd = 'rm '+rb.ruta_tmp+'/ambilight'
            os.system(cmd)
            pid = os.popen('pidof boblight-dispmanx').read()
            cmd ='kill -9 '+pid
            os.system(cmd)
            return "Ambilight desactivado"
        else:
            return "No dispone de sistema ambilight"
    if text == 'STATUS':
        if rb.ambi_v == True:
            return "Ambilight esta activado"
        else:
            return "Ambilight esta desactivado"

def modificar_rss(text,rb):
    if text == 'ON':
        rb.rss_v = True
        cmd = '> '+rb.ruta_tmp+'/rss'
        os.system(cmd)
        return "RSS activado"
    if text == 'OFF':
        rb.rss_v = False
        cmd = 'rm '+rb.ruta_tmp+'/rss'
        os.system(cmd)
        return "RSS desactivado"
    if text == 'ADD':
        rb.rssadd = True
        return 'Introduzca el nuevo feed'
    if text == 'DEL':
        rb.rssdel = True
        return 'Introduzca el numero que desea eliminar, si no los conoce use /rss list'
    if text == 'LIST':
        response = ''
        c = 1
        fpath = rb.ruta_config+'/listarss'
        if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            archivo = open(rb.ruta_config+'/listarss', 'r')
            for line in archivo.readlines():
                response += str(c)+' '+line
                c += 1
            archivo.close()
        else:
            response = "Lista vacia"
        return response
    if text == 'STATUS':
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

def comprobar_rss(text,rb):
    if rb.rssadd == True:
        aux = feedparser.parse(text)
        c = False
        fpath = rb.ruta_config+'/listarss'
        if not os.path.isfile(fpath):
            cmd = '> '+rb.ruta_tmp+'/listarss'
            os.system(cmd)
        try:
            response = "El feed "+aux.feed.title+" ha sido introducido"
            rb.listaurls.append(text)
            outfile = open(rb.ruta_config+'/listarss', 'a')
            outfile.write(text+'\n')
            outfile.close()
            rb.listarss.append(aux)
            rb.bdrss.append(rb.listarss[-1].entries[0].title)
        except:
            response = "[Error] El feed no existe"
        rb.rssadd = False
    if rb.rssdel == True:
        try:
            f = open(rb.ruta_config+'/listarss',"r")
            lineas = f.readlines()
            f.close()
            f = open(rb.ruta_config+'/listarss',"w")
            c = 1
            for linea in lineas:
                cont=str(c)
                if cont!=text:
                    f.write(linea)
                c += 1
            f.close()
            del rb.listaurls[int(text)-1]
            response = "Feed borrado"
        except:
            response = "[Error] Feed inexistente"
        rb.rssdel = False
    return response

def funcion_google(text):
    if(text[0] == '-'):
        num = text[1]
    else:
        num = 5
        lista = ''
        query = text.encode('utf-8')
        query = urllib.parse.urlencode ( { 'q' : query } )
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=%s&%s' % (num,query)
        search_response = urllib.request.urlopen(url)
        search_results = search_response.read()
        results = json.loads(search_results.decode("UTF-8"))
        data = results[ 'responseData' ]
        hits = data['results']
        for h in hits: lista+=(h['url']+'\n')
        return lista

def funcion_img(text,ruta_img):
    lista = []
    query = text.encode('utf-8')
    query = urllib.parse.urlencode ( { 'q' : query } )
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&rsz=8&%s' % query
    search_response = urllib.request.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results.decode("UTF-8"))
    data = results[ 'responseData' ]
    hits = data['results']
    for h in hits: lista.append(h['url'])
    f = open(ruta_img+'/image.jpg','wb')
    f.write(urllib.request.urlopen(random.choice(lista)).read())
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
