import os

class raspiBot():

	ambi_v = False
	rss_v = False
	rssadd = False
	rssdel = False
	torrent_v = False
	updating = False
	cont = 0
	contv = 3600
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
	ruta_ambi=str(os.popen("cat "+ruta_bot+"/config/ambi_path").read())
	#Ruta para el torrent
	filetorrent="/opt/torrentsend/torrentsended"

	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'
	ruta_config=ruta_bot+'/config'