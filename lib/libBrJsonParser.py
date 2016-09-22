# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
import urllib
#import dateutil.parser

pluginpath = 'plugin://script.module.libArd/'
chan = {"BR":"channel_28107",
		"br":"channel_28107",
		"ARD-Alpha":"channel_28487",
		"ardalpha":"channel_28487"}

def _parseMain():
	response = _utils.getUrl("http://www.br.de/system/halTocJson.jsp")
	j = json.loads(response)
	url = j["medcc"]["version"]["1"]["href"]
	response = _utils.getUrl(url)
	return json.loads(response)
	
def parseShows(letter):
	j = _parseMain()
	url = j["_links"]["broadcastSeriesAz"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)
	url = j['az']['_links'][letter.lower()]['href']
	response = _utils.getUrl(url)
	j = json.loads(response)
	list = []
	for show in j["_embedded"]["teasers"]:
		#xbmc.log(str(show))
		dict = {}
		dict['url'] = show["_links"]["self"]["href"]
		dict['name'] = show["headline"]
		dict['subtitle'] = show["topline"]
		if 'br-core:teaserText' in show["documentProperties"]:
			dict['plot'] = show["documentProperties"]["br-core:teaserText"]
		try: dict['thumb'] = show['teaserImage']['_links']['original']['href']
		except: pass
		dict['type'] = 'shows'
		dict['mode'] = 'libBrListVideos'
		
		list.append(dict)
	return list
	
def search(searchString):
	j = _parseMain()
	url = j["_links"]["search"]["href"].replace('{term}',urllib.quote_plus(searchString))
	return _parseLinks(url)
	
def parseVideos(url):
	if not 'latestVideos' in url:
		response = _utils.getUrl(url)
		j = json.loads(response)
		if "_links" in j and 'latestVideos' in j["_links"]:
			url = j["_links"]["latestVideos"]["href"]
		else: return []
	return _parseLinks(url)
	
def _parseLinks(url):
	response = _utils.getUrl(url)
	j = json.loads(response)
	list = []
	for show in j["_embedded"]["teasers"]:
		dict = {}
		dict['url'] = show["_links"]["self"]["href"]
		dict['name'] = show["topline"]
		if 'headline' in show:
			dict['name'] += ' - ' + show['headline']
			dict['tvshowtitle'] = show['topline']
			
		dict['subtitle'] = show["topline"]
		dict['plot'] = show["teaserText"]
		dict['channel'] = show["channelTitle"]
		duration = show['documentProperties']["br-core:duration"].split(':')
		dict['duration'] = int(duration[0]) * 3600 + int(duration[1]) * 60 + int(duration[2])
		dict['channel'] = show["channelTitle"]
		xbmc.log(str(show["teaserImage"]["_links"]))#image512
		if 'image512' in show["teaserImage"]["_links"]:
			dict['thumb'] = show["teaserImage"]["_links"]["image512"]["href"]
		elif 'image256' in show["teaserImage"]["_links"]:
			dict['thumb'] = show["teaserImage"]["_links"]["image256"]["href"]
		dict['type'] = 'video'
		dict['mode'] = 'libBrPlay'
		
		list.append(dict)
	try:
		dict = {}
		dict['type'] = 'nextPage'
		dict['url'] = j['_embedded']['_links']['next']['href']
		list.append(dict)
	except: pass
	return list
	
def parseDate(date,channel='BR'):
	j = _parseMain()
	#xbmc.log(str(j))
	url = j["_links"]["epg"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)
	url = j["epgDays"]["_links"][date]["href"]#date: 2016-12-30
	response = _utils.getUrl(url)
	j = json.loads(response)
	#xbmc.log(str(j))
	list = []
	broadcasts = j["channels"][chan[channel]]["broadcasts"]
	for b in broadcasts:
		if "_links" in b and "video" in b["_links"]:
			dict = {}
			dict["name"] = b["headline"]
			if len(b["subTitle"]) > 0:
				dict['name'] += ' - ' + b["subTitle"]
			dict["plot"] = b["subTitle"]
			dict["subtitle"] = b["hasSubtitle"]
			dict["url"] = b["_links"]["video"]["href"]
			dict["time"] = startTimeToInt(b["broadcastStartDate"][11:19])
			dict['date'] = b["broadcastStartDate"][11:16]
			dict['duration'] = (startTimeToInt(b["broadcastEndDate"][11:19]) - startTimeToInt(b["broadcastStartDate"][11:19])) * 60
			if dict['duration'] < 0:
				dict['duration'] = 86400 - abs(dict['duration'])
			#TODO: rest of properties
			dict['type'] = 'date'
			dict['mode'] = 'libBrPlay'
			list.append(dict)
	return list
			
	
def parse(url):
	list = []
	response = _utils.getUrl(url)
	j = json.loads(response)

def parseVideo(url):#TODO grep the plot and other metadata from here
	response = _utils.getUrl(url)
	j = json.loads(response)
	assets = j["assets"]
	for asset in assets:
		if "type" in asset and asset["type"] == "HLS_HD":
			return asset["_links"]["stream"]["href"]
	for asset in assets:
		if "type" in asset and asset["type"] == "HLS":
			return asset["_links"]["stream"]["href"]
			
def startTimeToInt(s):
	HH,MM,SS = s.split(":")
	return int(HH) * 60 + int(MM)