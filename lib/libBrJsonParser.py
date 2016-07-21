# -*- coding: utf-8 -*-
import xbmc
import json
import _utils
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
		dict = {}
		dict['url'] = show["_links"]["self"]["href"]
		dict['name'] = show["headline"]
		dict['subtitle'] = show["topline"]
		if 'br-core:teaserText' in show["documentProperties"]:
			dict['plot'] = show["documentProperties"]["br-core:teaserText"]
		#dict['thumb'] = show["teaserImage"]["_links"]["image480q"]["href"]
		
		dict['type'] = 'dir'
		dict['mode'] = 'libBrListVideos'
		
		list.append(dict)
	return list
	
def parseVideos(url):
	response = _utils.getUrl(url)
	j = json.loads(response)
	url = j["_links"]["latestVideos"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)
	list = []
	for show in j["_embedded"]["teasers"]:
		dict = {}
		dict['url'] = show["_links"]["self"]["href"]
		dict['name'] = show["headline"]
		dict['subtitle'] = show["topline"]
		dict['plot'] = show["teaserText"]
		dict['thumb'] = show["teaserImage"]["_links"]["image480q"]["href"]
		
		dict['type'] = 'video'
		dict['mode'] = 'libBrPlay'
		
		list.append(dict)
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
		xbmc.log(str(b))
		if "_links" in b and "video" in b["_links"]:
			dict = {}
			
			dict["name"] = b["headline"]
			dict["plot"] = b["subTitle"]
			dict["subtitle"] = b["hasSubtitle"]
			dict["url"] = b["_links"]["video"]["href"]
			dict["time"] = startTimeToInt(b["broadcastStartDate"][11:19])
			#TODO: rest of properties
			dict['type'] = 'video'
			dict['mode'] = 'libBrPlay'
			list.append(dict)
	return list
			
	
def parse(url):
	list = []
	response = _utils.getUrl(url)
	j = json.loads(response)

def parseVideo(url):
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