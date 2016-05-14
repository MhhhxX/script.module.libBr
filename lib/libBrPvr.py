import libBrJsonParser,libBr
import xbmc,xbmcgui

def play(dict):
	video = _searchEpisode(dict)
	
	if not video:
		xbmc.executebuiltin("Notification(Kein Video gefunden,Nicht in Mediathek, 7000)")
		xbmc.log("no video found")
		return
	xbmc.log(str(video))
	url = libBr.getVideoUrl(video["url"])
	#listitem = xbmcgui.ListItem(label=video["name"],thumbnailImage=video["thumb"],path=url)
	listitem = xbmcgui.ListItem(label=video["name"],path=url)
	xbmc.Player().play(url, listitem)
		
def _searchEpisode(dict):
	video = False
	entries = libBrJsonParser.parseDate(dict["date"])
	for entry in entries:
		if dict["time"] == entry["time"]:
			video = entry
	return video
			