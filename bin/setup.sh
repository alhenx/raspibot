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
restartscript="/usr/local/bin/restartraspibot.sh"
service="raspibot.service"
user=$(echo $USER)

keepon=true

while $keepon ;
do
	echo -e "**************************************************"
	echo -e "******* RaspiBot Beta Bermellón (de China) *******"
	echo -e "**************************************************"
	echo -e "Introduzca el número de la opción deseada del programa:\n"
	echo -e "\t1. Instalación de RaspiBot."
	echo -e "\t2. Actualización de RaspiBot."
	echo -e "\t3. Desinstalación de RaspiBot."
	echo -e "\t4. Consultar estado de RaspiBot."
	echo -e "\t5. Salir."
	read x
		case $x in
			1)
				echo "******* INSTALACIÓN SELECCIONADA *******"
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

				echo "Instalando RaspiBot..."
				git clone https://github.com/alhenx/raspibot.git $botpath --quiet

				echo "A continuación se configurarán algunos archivos..."
				mkdir $botpath/tmp

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
				mkdir $botpath/config

				echo -n $token_bot > $botpath/config/token_bot
				echo -n $chat_id > $botpath/config/chat_id

				if [ $(echo $ambi_path | wc -l) == 1 -a $(echo $ambi_path) != "" ] ; then
					echo -n $ambi_path > $botpath/config/ambi_path
				else
					echo -n "NOPE" > $botpath/config/ambi_path
				fi

				sudo chmod 444 $botpath/config/*

				echo -e "\nComprobando si cuenta con $torrent en el sistema..."
				if (sudo pacman -Q $torrent >/dev/null 2>&1) ; then
					echo "Se ha detectado $torrent instalado en el sistema."
					echo "A continuación es necesario introducir el usuario y contraseña"
					echo "del servicio para $torrent web. Introduzca su usuario:"
					read torrentuser

					echo -e "\nIntroduzca la contraseña:"
					read torrentpass

					echo "Se añadirá este servicio a la lista de alertas de RaspiBot."

					sudo sed -i 's^"script-torrent-done-enabled": false,^"script-torrent-done-enabled": true,^g' $torrentsettings
  				sudo sed -i 's^"script-torrent-done-filename": "",^"script-torrent-done-filename": "'"$torrentalertscript"'",^g' $torrentsettings

  				echo -e '#!/bin/bash' | sudo tee $torrentalertscript >/dev/null
  				echo -e 'torrentsalertfile="'"$torrentsfile"'"' | sudo tee --append $torrentalertscript >/dev/null
  				echo -e 'echo $TR_TORRENT_NAME > $torrentsalertfile' | sudo tee --append $torrentalertscript >/dev/null
  				echo -e "exit 0" | sudo tee --append $torrentalertscript >/dev/null

  				sudo systemctl reload transmission

  				sudo chmod a+x $torrentalertscript
  				echo -n $torrentuser > $botpath/config/torrentuser
					echo -n $torrentpass > $botpath/config/torrentpass
				fi

				echo -e "#!/bin/bash" | sudo tee $restartscript >/dev/null
				echo -e "/usr/bin/systemctl restart $service" | sudo tee --append $restartscript >/dev/null
				sudo chmod 500 $restartscript
				echo -e "$user ALL=(ALL) NOPASSWD: $restartscript" | sudo tee --append /etc/sudoers >/dev/null

				sudo ln -s $botpath/bin/raspibot /bin/raspibot

				echo "[Unit]" > $botpath/$service
				echo "Description=RaspiBot for Telegram" >> $botpath/$service
				echo "" >> $botpath/$service
				echo "[Service]" >> $botpath/$service
				echo "User=$user" >> $botpath/$service
				echo "Type=oneshot" >> $botpath/$service
				echo "ExecStart=raspibot exec" >> $botpath/$service
				echo "TimeoutSec=0" >> $botpath/$service
				echo "RemainAfterExit=yes" >> $botpath/$service
				echo "" >> $botpath/$service
				echo "[Install]" >> $botpath/$service
				echo "WantedBy=multi-user.target" >> $botpath/$service

				sudo mv $botpath/$service /usr/lib/systemd/system/

				sudo systemctl enable $service

				sudo systemctl start $service

				echo -e "\nSe ha creado, activado e iniciado el servicio 'raspibot'."
				echo "Puede consultar su estado con 'sudo systemctl status $service'"
				echo "Proceso de instalación completado. RaspiBot instalado."
				keepon=false
			;;
			### END CASE 1
			2)
				echo "******* ACTUALIZACIÓN SELECCIONADA *******"
				echo "Comprobando actualizaciones..."
				localversion=$(cat $botpath/version)
				remoteversion=$(curl -s https://raw.githubusercontent.com/alhenx/raspibot/master/version)
				if [ "$localversion" != "$remoteversion" ]; then
					echo "Existe una nueva versión de RaspiBot. Actualizando..."
					mv $botpath $botpath_bak
					git clone https://github.com/alhenx/raspibot.git $botpath --quiet
					echo "Configurando RaspiBot..."
					cp -r $botpath_bak/config $botpath
					cp -r $botpath_bak/tmp $botpath
					touch $botpath/tmp/update
					echo "Eliminando versiones anteriores..."
					rm -rf $botpath_bak
					oldexecfile="$botpath_bak/raspibot.sh"
					if [ -f $oldexecfile ] ; then
						rm -f $oldexecfile
						if [ ! -f /bin/raspibot ] ; then
							sudo ln -s $botpath/bin/raspibot /bin/raspibot
						fi
						sudo sed -i 's^ExecStart='"$execfile"'^ExecStart=raspibot exec^g' /usr/lib/systemd/system/$service
					fi
					if [ ! -f $restartscript ] ; then
						echo -e "#!/bin/bash" | sudo tee $restartscript >/dev/null
						echo -e "/usr/bin/systemctl restart $service" | sudo tee --append $restartscript >/dev/null
						sudo chmod 500 $restartscript
						echo -e "$user ALL=(ALL) NOPASSWD: $restartscript" | sudo tee --append /etc/sudoers >/dev/null
					fi
					if [ ! -f $botpath/config/torrentuser ] ; then
						echo "Se ha detectado $torrent instalado en el sistema, pero no"
						echo "está configurado para utilizarse mediante RaspiBot."
						echo "A continuación es necesario introducir el usuario y contraseña"
						echo "del servicio para $torrent web. Introduzca su usuario:"
						read torrentuser

						echo -e "\nIntroduzca la contraseña:"
						read torrentpass

	  				echo -n $torrentuser > $botpath/config/torrentuser
						echo -n $torrentpass > $botpath/config/torrentpass
					fi
					raspibot restart
					echo "Actualización completada."
				else
					echo "No hay actualizaciones disponibles para RaspiBot."
				fi
				keepon=false
			;;
			### END CASE 2
			3)
				echo "******* DESINSTALACIÓN SELECCIONADA *******"
				echo "Comenzando proceso de desinstalación..."
				sudo rm -rf $installdir >/dev/null 2>&1
				sudo rm -rf $torrentendpath > /dev/null 2>&1
				sudo systemctl stop $service >/dev/null 2>&1
				sudo systemctl disable $service >/dev/null 2>&1
				sudo rm /usr/lib/systemd/system/$service >/dev/null 2>&1
				sudo rm -f /bin/raspibot >/dev/null 2>&1
				sudo rm -f $restartscript >/dev/null 2>&1
				echo "Desinstalación completada."
				keepon=false
			;;
			### END CASE 3
			4)
				echo "Comprobando estado..."
				sudo systemctl status $service
				keepon=false
			;;
			### END CASE 4
			5)
				keepon=false
				echo "Saliendo..."
			;;
			*)
				echo "La opción seleccionada no es válida."
			;;
		esac
done

#end
