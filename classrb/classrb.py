import os

class raspiBot():

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

	#Ruta del bot
	ruta_bot="/opt/raspibot-setup/raspibot"

	#TOKEN del bot
	API_TOKEN=os.popen("cat "+ruta_bot+"/config/token_bot").read()

	#Identificador del chat
	ID=int(os.popen("cat "+ruta_bot+"/config/chat_id").read())

	#Ruta del ambilight
	ruta_ambi=os.popen("find / -name 'boblight-dispmanx' 2>&1 | grep -v 'find:'").read()

	#Ruta para el torrent
	filetorrent="/opt/torrentsend/torrentsended"

	#Lista de feeds para el RSS
	listaurls.append('http://feeds.feedburner.com/linuxenandalu?format=xml')
	istaurls.append('http://blogdesuperheroes.es/feed')
 	listaurls.append('http://feeds.weblogssl.com/vayatele2?format=xml')


	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'
