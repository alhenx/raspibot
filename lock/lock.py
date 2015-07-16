import feedparser
import os

def lock_torrent(rb):
    file = rb.ruta_tmp+"/torrent"
    fileexists = os.path.isfile(file)
    if fileexists:
        rb.torrent_v = True
    else:
        rb.torrent_v = False

def lock_rss(rb):
    file = rb.ruta_tmp+"/rss"
    fileexists = os.path.isfile(file)
    if fileexists:
        rb.rss_v = True
    else:
        rb.rss_v = False

def lock_ambi(rb):
    file = rb.ruta_tmp+"/ambilight"
    fileexists = os.path.isfile(file)
    if fileexists:
        rb.ambi_v = True
        cmd = '> '+rb.ruta_tmp+'/ambilight'
        os.system(cmd)
        cmd = rb.ruta_ambi+' -o saturation=2.0 -p 100 -f /dev/null > /dev/null'
        os.system(cmd)
    else:
        rb.ambi_v = False

def setup_ini(rb):
    lock_rss(rb)
    lock_ambi(rb)
    lock_torrent(rb)
    for i in range(0,len(rb.listaurls)):
        rb.listarss.append(feedparser.parse(rb.listaurls[i]))
    for i in range(0,len(rb.listarss)):
        rb.bdrss.append(rb.listarss[i].entries[0].title)
