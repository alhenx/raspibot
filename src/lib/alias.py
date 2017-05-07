#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from subprocess import Popen, PIPE

def getList():
	cmd='cat ~/.*rc | grep -P \'^alias\'| sed \'s/alias //g\' | cut -d= -f1'
	stdout=Popen(['/bin/bash', '-i', '-c', cmd],stdout=PIPE,stderr=PIPE).communicate()[0].decode()
	return stdout.splitlines()

def runAlias(cmd):
	return Popen(['/bin/bash', '-i', '-c', cmd],stdout=PIPE,stderr=PIPE).communicate()[0].decode()