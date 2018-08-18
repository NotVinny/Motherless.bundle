from MLCommon import *
from MLGroups import *
from MLTags import *
from MLMembers import *

CHANNEL_NAME =	'Motherless'

DEFAULT_ART =		'art-' + Prefs["channelBackgroundArt"]
DEFAULT_ICON =		'icon-' + Prefs["channelIconArt"]

def Start():
	
	# Set the defaults for Object Containers
	ObjectContainer.title1 =	CHANNEL_NAME
	ObjectContainer.art =		R(DEFAULT_ART)
	
	# Set the defaults of Directory Objects
	DirectoryObject.thumb =	R(DEFAULT_ICON)
	VideoClipObject.thumb =	R(DEFAULT_ICON)
	PhotoObject.thumb =		R(DEFAULT_ICON)
	
	# Set the cache lifespan
	HTTP.CacheTime =		CACHE_1HOUR * 2
	
	# Set the user agent
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.3 (KHTML, like Gecko) Version/8.0.1 Safari/600.2.3'

def ValidatePrefs():
	DEFAULT_ART =		'art-' + Prefs["channelBackgroundArt"]
	ObjectContainer.art =		R(DEFAULT_ART)
	
	DEFAULT_ICON =		'icon-' + Prefs["channelIconArt"]
	DirectoryObject.thumb =	R(DEFAULT_ICON)

@handler(ML_ROUTE_PREFIX, CHANNEL_NAME, thumb=DEFAULT_ICON, art=DEFAULT_ART)
def MainMenu():
	
	# Create a dictionary of menu items
	mainMenuItems = OrderedDict([
		('Browse All Videos',	{'function':BrowseVideos}),
		('Groups',				{'function':BrowseGroups}),
		('Tags',				{'function':ListTags}),
		('Members',			{'function':BrowseMembers}),
		('Search',				{'function':SearchTags, 'search':True, 'directoryObjectArgs':{'prompt':'Search for...','summary':'Enter Search Terms'}})
	])
	
	oc = GenerateMenu(CHANNEL_NAME, mainMenuItems)
	
	oc.add(PrefsObject(
		title="Preferences"
	))
	
	return oc