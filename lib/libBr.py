# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urllib
import libBrJsonParser

def getDate(date):
	return listing.parseDate(date)
def getVideoUrl(url):
	return libBrJsonParser.parseVideo(url)
	
	

def libBrPvrPlay(dict):
	import libBrPvr
	libBrPvr.play(dict)