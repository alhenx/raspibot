import os

class raspiBot():

	torrent_m = False
	ambi_m = False
	rss_m = False
	ambi_v = False
	rss_v = False
	rssadd = False
	torrentadd = False
	torrentdel = False
	rssdel = False
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
	ruta_ambi=str(os.popen("cat "+ruta_bot+"/config/ambi_path").read())
	#Ruta para el torrent
	filetorrent="/opt/torrentsend/torrentsended"

	torrent_user=str(os.popen("cat "+ruta_bot+"/config/torrentuser").read())
	torrent_pass=str(os.popen("cat "+ruta_bot+"/config/torrentpass").read())

	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'
	ruta_config=ruta_bot+'/config'