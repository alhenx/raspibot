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
	API_TOKEN=str(os.popen("cat "+ruta_bot+"/config/token_bot").read())

	#Identificador del chat
	ID=int(os.popen("cat "+ruta_bot+"/config/chat_id").read())

	#Ruta del ambilight
	ruta_ambi=str("cat "+ruta_bot+"/config/ambi_path").read())
	#Ruta para el torrent
	filetorrent="/opt/torrentsend/torrentsended"

	#Lista de feeds para el RSS
	listaurls.append('http://feeds.feedburner.com/linuxenandalu?format=xml')
	listaurls.append('http://blogdesuperheroes.es/feed')
 	listaurls.append('http://feeds.weblogssl.com/vayatele2?format=xml')


	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'
