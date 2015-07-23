#!/bin/bash

# Script de instalación de RaspiBot.
# Raúl Díez Sánchez - Alejandro Chacón Peregrino.

#ATENCIÓN: NO EDITAR ESTE FICHERO.

installdir="/opt/raspibot-setup"
botpath="$installdir/raspibot"
botpath_bak="$botpath-bak"
torrentendpath="/opt/torrentsend"
torrentsfile="$torrentendpath/torrentsended"
execfile="$botpath/raspibot.sh"
ambilight="boblight-dispmanx"
torrent="transmission-cli"
torrentsettings="/var/lib/transmission/.config/transmission-daemon/settings.json"
torrentalertscript="/usr/bin/torrent-finished.sh"
service="raspibot.service"
user=$(echo $USER)

echo -e "**************************************************"
echo -e "******* RaspiBot Beta Bermellón (de China) *******"
echo -e "**************************************************"
echo -e "Introduzca el número de la opción deseada del programa:\n"
echo -e "\t1. Instalación de RaspiBot."
echo -e "\t2. Actualización de RaspiBot."
echo -e "\t3. Desinstalación de RaspiBot."
echo -e "\t4. Consultar estado de RaspiBot."
echo -e "\t5. Salir."

keepon=true

while $keepon ;
do
	read x
		case $x in
			1)
				echo "Comenzando proceso de instalación..."
				sleep 0.5
				echo "Sincronizando las bases de datos de los paquetes..."
				sudo pacman -Syy >/dev/null

				echo "Comprobando paquetes necesarios del sistema."

				pypkg="python"
				pippkg="python-pip"

				if !(sudo pacman -Q $pypkg >/dev/null 2>&1) ; then
					echo "Instalando $pypkg..."
					sudo pacman -S $pypkg --noconfirm >/dev/null
				fi

				if !(sudo pacman -Q $pippkg >/dev/null 2>&1) ; then
					echo "Instalando $pippkg..."
					sudo pacman -S $pippkg --noconfirm >/dev/null
				fi

				echo "Comprobando módulos pip."
				pipmodules[0]=pyTelegramBotAPI
				pipmodules[1]=wikipedia
				pipmodules[2]=feedparser

				for (( i=0; i<${#pipmodules[@]}; i++ ))
				do
					if ! pip list | grep ${pipmodules[$i]} >/dev/null ; then
						echo "Instalando módulo ${pipmodules[$i]}..."
						sudo pip install ${pipmodules[$i]} >/dev/null
					fi
				done

				echo "Creando directorios necesarios para la instalación..."
				sudo mkdir -p $installdir
				sudo mkdir -p $torrentendpath
				sudo chmod a+wx $installdir
				sudo chmod a+wx $torrentendpath
				cd $installdir

				echo "Instalando RaspiBot..."
				git clone https://github.com/alhenx/raspibot.git --quiet

				echo "A continuación se configurarán algunos archivos..."
				cd $botpath
				echo "#!/bin/bash" > $execfile
				echo "python $installdir/raspibot/raspibot.py &" >> $execfile
				sudo chmod a+x $execfile

				mkdir tmp

				token_bot=
				while [[ $token_bot == "" ]]; do
					echo "Por favor, introduzca el API_TOKEN (no puede dejarse en blanco)"
					echo "de su Bot (se la facilitará @BotFather al crear su Bot):"
					read token_bot
				done

				sleep 0.5
				chat_id=
				while [[ $chat_id == "" ]]; do
					echo -e "\nPor favor, introduzca su CHAT_ID (no puede dejarse en blanco)."
					echo "Si no tiene uno, o no lo recuerda, póngase en contacto con @CabashiBot"
					echo "mediante Telegram, y envíele el comando '/chatid' (sin las comillas)."
					read chat_id
				done

				sleep 0.5

				echo -e "\nComprobando si cuenta con $ambilight en el sistema..."
				ambi_path=$(find / -type f -name $ambilight 2>&1 | grep -v 'find:')

				sleep 0.5
				mkdir config

				echo -n $token_bot > config/token_bot
				echo -n $chat_id > config/chat_id

				if [ $(echo $ambi_path | wc -l) == 1 ] ; then
					echo -n $ambi_path > config/ambi_path
				else
					echo -n "NOPE" > config/ambi_path
				fi

				sudo chmod 444 config/*

				echo -e "\nComprobando si cuenta con $torrent en el sistema..."
				if (sudo pacman -Q $torrent >/dev/null 2>&1) ; then
					echo "Se ha detectado $torrent instalado en el sistema."
					echo "Se añadirá este servicio a la lista de alertas de RaspiBot."

					sudo sed -i 's^"script-torrent-done-enabled": false,^"script-torrent-done-enabled": true,^g' $torrentsettings
	    		sudo sed -i 's^"script-torrent-done-filename": "",^"script-torrent-done-filename": "'"$torrentalertscript"'",^g' $torrentsettings

	    		echo -e '#!/bin/bash' | sudo tee $torrentalertscript >/dev/null
	    		echo -e 'torrentsalertfile="'"$torrentsfile"'"' | sudo tee --append $torrentalertscript >/dev/null
	    		echo -e 'echo $TR_TORRENT_NAME > $torrentsalertfile' | sudo tee --append $torrentalertscript >/dev/null
	    		echo -e "exit 0" | sudo tee --append $torrentalertscript >/dev/null

	    		sudo chmod a+x $torrentalertscript
				fi

				echo "[Unit]" > $service
				echo "Description=RaspiBot for Telegram" >> $service
				echo "" >> $service
				echo "[Service]" >> $service
				echo "User=$user" >> $service
				echo "Type=oneshot" >> $service
				echo "ExecStart=$execfile" >> $service
				echo "TimeoutSec=0" >> $service
				echo "RemainAfterExit=yes" >> $service
				echo "" >> $service
				echo "[Install]" >> $service
				echo "WantedBy=multi-user.target" >> $service

				sudo mv $service /usr/lib/systemd/system/

				sudo systemctl enable $service

				sudo systemctl start $service

				echo -e "\nSe ha creado, activado e iniciado el servicio 'raspibot'."
				echo "Puede consultar su estado con 'sudo systemctl status $service'"
				echo "Proceso de instalación completado. RaspiBot instalado."
				keepon=false
			;;
			### END CASE 1
			2)
				echo "Comprobando actualizaciones..."
				localversion=$(cat $botpath/version)
				remoteversion=$(curl -s https://raw.githubusercontent.com/alhenx/raspibot/master/version)
				if [ "$localversion" != "$remoteversion" ]; then
					echo "Existe una nueva versión de RaspiBot. Actualizando..."
					cd $installdir
					mv $botpath $botpath_bak
					git clone https://github.com/alhenx/raspibot.git --quiet
					echo "Configurando RaspiBot..."
					cp -r $botpath_bak/config $botpath
					cp -r $botpath_bak/tmp $botpath
					cd $botpath
					echo "#!/bin/bash" > $execfile
					echo "python $installdir/raspibot/raspibot.py &" >> $execfile
					sudo chmod a+x $execfile
					touch $botpath/tmp/update
					echo "Eliminando versiones anteriores..."
					rm -rf $botpath_bak
					sudo systemctl restart raspibot.service
					echo "Actualización completada."
				else
					echo "No hay actualizaciones disponibles para RaspiBot."
				fi
				keepon=false
			;;
			### END CASE 2
			3)
				echo "Comenzando proceso de desinstalación..."
				sudo rm -rf $installdir >/dev/null 2>&1
				sudo rm -rf $torrentendpath > /dev/null 2>&1
				sudo systemctl stop raspibot >/dev/null 2>&1
				sudo systemctl disable raspibot >/dev/null 2>&1
				sudo rm /usr/lib/systemd/system/raspibot.service >/dev/null 2>&1
				echo "Desinstalación completada."
				keepon=false
			;;
			### END CASE 3
			4)
				echo "Comprobando estado..."
				sudo systemctl status raspibot
				keepon=false
			;;
			### END CASE 4
			5)
				keepon=false
				echo "Saliendo..."
			;;
			*)
				echo "La opción seleccionada no es válida."
				echo -e "Introduzca el número de la opción deseada del programa:\n"
				echo -e "\t1. Instalación de RaspiBot."
				echo -e "\t2. Actualización de RaspiBot."
				echo -e "\t3. Desinstalación de RaspiBot."
				echo -e "\t4. Consultar estado de RaspiBot."
				echo -e "\t5. Salir."
			;;
		esac
done

#end
