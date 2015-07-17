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
    file2 = rb.ruta_config+"/listarss"
    fileexists = os.path.isfile(file)
    file2exists = os.path.isfile(file2)
    if fileexists:
        rb.rss_v = True
        if file2exists:
            archivo = open(rb.ruta_config+'/listarss', 'r')
            for linea in archivo.readlines():
                rb.listaurls.append(linea)
                aux = feedparser.parse(linea)
                rb.listarss.append(aux)
                rb.bdrss.append(rb.listarss[-1].entries[0].title)
            archivo.close()
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

