# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib
import libBrJsonParser
import libMediathek
from datetime import date, timedelta

translation = xbmcaddon.Addon(id='script.module.libMediathek').getLocalizedString





def getDate(date,channel='BR'):
	return libBrJsonParser.parseDate(date,channel)
def search(searchString):
	return libBrJsonParser.search(searchString)
def getVideoUrl(url):
	return libBrJsonParser.parseVideo(url)
def play(dict):
	url = getVideoUrl(dict["url"])
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=dict["name"],path=url)
	xbmc.Player().play(url, listitem)	
	

def libBrPvrPlay(dict):
	import libBrPvr
	libBrPvr.play(dict)
	
def libBrListMain():
	dict = []
	#dict.append({'name':translation(31030), 'mode':'libBrListVideos', 'url':''})
	dict.append({'name':translation(31032), 'mode':'libBrListLetters'})
	dict.append({'name':translation(31033), 'mode':'libBrListDate'})
	dict.append({'name':translation(31039), 'mode':'libBrSearch'})
	libMediathek.addEntries(dict)
	#libMediathek.addEntry({'name':translation(31034), 'mode':'libArdListVideos', 'url':'http://www.ardmediathek.de/appdata/servlet/tv/Rubriken/mehr?documentId=21282550&json'})
	
	
	
def libBrListLetters():
	libMediathek.populateDirAZ('libBrListShows')
	
def libBrListShows():
	libMediathek.addEntries(libBrJsonParser.parseShows(params['name']))
	
def libBrListVideos():
	libMediathek.addEntries(libBrJsonParser.parseVideos(params['url']))

def libBrListDate():
	libMediathek.populateDirDate('libBrListDateChannels')
	
def libBrListDateChannels():
	xbmc.log(str(params))
	libMediathek.addEntry({'name':'ARD-Alpha', 'mode':'libBrListDateVideos', 'datum': params['datum']})
	libMediathek.addEntry({'name':'BR', 'mode':'libBrListDateVideos', 'datum': params['datum']})

def libBrListDateVideos():
	datum = date.today() - timedelta(int(params['datum']))
	xbmc.log(datum.strftime('%Y-%m-%d'))
	libMediathek.addEntries(libBrJsonParser.parseDate(datum.strftime('%Y-%m-%d'),params['name']))#params['datum'] =yyyy-mm-dd
	
def libBrSearch():
	keyboard = xbmc.Keyboard('', translation(31039))
	keyboard.doModal()
	if keyboard.isConfirmed() and keyboard.getText():
		search_string = keyboard.getText()
		libBrListSearch(search_string)

def libBrListSearch(searchString=False):
	if not searchString:
		searchString = params['searchString']
	libMediathek.addEntries(search(searchString))
	
def libBrPlay():
	url = libBrJsonParser.parseVideo(params['url'])
	xbmc.log(url)
	listitem = xbmcgui.ListItem(path=url)
	xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)
	
	
def list():	
	modes = {
	'libBrListLetters': libBrListLetters,
	'libBrListShows': libBrListShows,
	'libBrListVideos': libBrListVideos,
	'libBrListDate': libBrListDate,
	'libBrListDateChannels': libBrListDateChannels,
	'libBrListDateVideos': libBrListDateVideos,
	'libBrSearch': libBrSearch,
	'libBrListSearch': libBrListSearch,
	'libBrPlay': libBrPlay
	}
	views = {
	'libBrListShows': 'shows',
	'libBrListVideos': 'videos',
	'libBrListDate': 'videos',
	'libBrListDateVideos': 'videos',
	'libBrListSearch': 'videos'
	}
	global params
	params = libMediathek.get_params()
	global pluginhandle
	pluginhandle = int(sys.argv[1])
	
	if not params.has_key('mode'):
		libBrListMain()
	else:
		modes.get(params['mode'],libBrListMain)()
		libMediathek.setView(views.get(params['mode'],'default'))
	xbmcplugin.endOfDirectory(int(sys.argv[1]))	