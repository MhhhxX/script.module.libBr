# -*- coding: utf-8 -*-
import xbmc
import json
import _utils

pluginpath = 'plugin://script.module.libArd/'
chan = {"br":"channel_28107"}

def parseDate(date):
	c = "br"#TODO
	response = _utils.getUrl("http://www.br.de/system/halTocJson.jsp")
	j = json.loads(response)
	url = j["medcc"]["version"]["1"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)

	xbmc.log(str(j))
	url = j["_links"]["epg"]["href"]
	response = _utils.getUrl(url)
	j = json.loads(response)
	url = j["epgDays"]["_links"][date]["href"]#date: 2016-12-30
	response = _utils.getUrl(url)
	j = json.loads(response)
	
	list = []
	broadcasts = j["channels"][chan[c]]["broadcasts"]
	for b in broadcasts:
		if "_links" in b and "video" in b["_links"]:
			dict = {}
			
			dict["name"] = b["headline"]
			dict["plot"] = b["subTitle"]
			dict["subtitle"] = b["hasSubtitle"]
			dict["url"] = b["_links"]["video"]["href"]
			dict["time"] = startTimeToInt(b["broadcastStartDate"][11:19])
			#TODO: rest of properties
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
			#xbmc.log(asset["_links"]["stream"])
			return asset["_links"]["stream"]["href"]
			
def startTimeToInt(s):
	HH,MM,SS = s.split(":")
	return int(HH) * 60 + int(MM)