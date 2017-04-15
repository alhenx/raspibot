#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import json

jsonFile = "/opt/raspibot-setup/raspibot/"

with open(jsonFile+'data.json') as json_data:
	d = json.load(json_data)
	userTorrent = d["torrent-user"]
	passTorrent = d["torrent-pass"]

def getList():
	cmd = "transmission-remote -n "+userTorrent+":"+passTorrent+" -l | sed -e \'1d;$d;s/^ *//\' | awk \'{print $1 \"\\t\" substr($0,index($0,$10))\"\\n\"}\'"
	return os.popen(cmd).read()

def addTorrent(torrentLink):
	cmd = "transmission-remote -n "+userTorrent+":"+passTorrent+" -a \""+torrentLink+"\""
	responseTransmission = os.popen(cmd).read()
	if responseTransmission.startswith('Error'):
		responseTransmission = "Magnet invalido"
		return responseTransmission
	return "Torrent added"

def delTorrent(torrentId):
	cmd = "transmission-remote -n "+userTorrent+":"+passTorrent+" -t "+torrentId+" -r"
	os.system(cmd)
	return "Torrent "+torrentId+" deleted"