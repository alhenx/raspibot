#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import os
import json

jsonFile = os.getcwd()

with open(jsonFile+'/data.json') as json_data:
	d = json.load(json_data)
	userTorrent = d["torrent-user"]
	passTorrent = d["torrent-pass"]

def getList(type):
	cmd = "transmission-remote -n "+userTorrent+":"+passTorrent+" -l |sed -e \'s/ kB\| MB\| GB\| TB//g\'|sed -e \'1d;$d;s/^ *//\'| awk \'{print $1 \"\\t\" substr($0,index($0,$9))}\'"
	responseTransmission = os.popen(cmd).read()
	listTorrent = responseTransmission.splitlines()
	matrixTorrent = [[] for i in range(len(listTorrent))]
	for i in range(len(listTorrent)):
		matrixTorrent[i] = listTorrent[i].split("\t")
	if type==0:
		stringTorrent = ""
		for i in range(len(listTorrent)):
			stringTorrent+=matrixTorrent[i][1]+"\n\n"
		return stringTorrent
	if type==1:
		return matrixTorrent

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