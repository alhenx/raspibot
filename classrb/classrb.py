
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

	#TOKEN del bot
	API_TOKEN=''

	#Identificador del chat
	ID=

	#Ruta del bot
	ruta_bot=''

	#Ruta del ambilight
	ruta_ambi=''

	#Ruta para el torrent
	filetorrent=''

	#Lista de feeds para el RSS
	listaurls.append('http://feeds.feedburner.com/linuxenandalu?format=xml')



	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'