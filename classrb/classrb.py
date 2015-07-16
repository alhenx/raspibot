
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
	API_TOKEN='91624969:AAGpeA5uSr8kdr41pdZ_yJKPUux59tanprQ'

	#Identificador del chat
	ID=2011846

	#Ruta del bot
	ruta_bot='/opt/raspibot-setup/raspibot'

	#Ruta del ambilight
	ruta_ambi='/home/alhen/boblight-archarm/boblight-dispmanx'

	#Ruta para el torrent
	filetorrent='/opt/torrentsend/torrentsended'

	#Lista de feeds para el RSS
	listaurls.append('http://feeds.feedburner.com/linuxenandalu?format=xml')
	listaurls.append('http://blogdesuperheroes.es/feed')
	listaurls.append('http://feeds.weblogssl.com/vayatele2?format=xml')
	listaurls.append('http://alhenbot.blogspot.com.es/feeds/posts/default')



	#######################################################

	ruta_tmp=ruta_bot+'/tmp'
	ruta_img=ruta_bot+'/img'