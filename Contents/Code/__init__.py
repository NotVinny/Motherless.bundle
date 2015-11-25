from MLCommon import *
from MLBrowseVideos import *
from MLGroups import *
from MLTags import *
from MLMembers import *

CHANNEL_NAME =	'Motherless'

DEFAULT_ART =		'art-default.jpg'
DEFAULT_ICON =		'icon-default.jpg'

def Start():
	
	# Set the defaults for Object Containers
	ObjectContainer.title1 =	CHANNEL_NAME
	ObjectContainer.art =		R(DEFAULT_ART)
	
	# Set the defaults of Directory Objects
	DirectoryObject.thumb =	R(DEFAULT_ICON)
	
	# Set the cache lifespan
	HTTP.CacheTime =		CACHE_1HOUR * 2
	
	# Set the user agent
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.3 (KHTML, like Gecko) Version/8.0.1 Safari/600.2.3'

@handler(ML_ROUTE_PREFIX, CHANNEL_NAME, thumb=DEFAULT_ICON, art=DEFAULT_ART)
def MainMenu():
	
	# Create the object to contain the main menu options
	oc = ObjectContainer()
	
	# TODO: Use some data structure to make this into a loop... A simple dictionary won't do, will need to ponder this. First change to be made for v1.3
	
	# Directory Object for Browse All Videos
	oc.add(DirectoryObject(
		key =	Callback(BrowseVideos, title='Browse All Videos'),
		title =	'Browse All Videos'
	))
	
	# Directory Object for Groups
	oc.add(DirectoryObject(
		key =	Callback(BrowseGroups, title='Groups'),
		title =	'Groups'
	))
	
	# Directory Object for Tags
	oc.add(DirectoryObject(
		key =	Callback(BrowseTags, title='Tags'),
		title =	'Tags'
	))
	
	# Directory Object for Members
	oc.add(DirectoryObject(
		key =	Callback(BrowseMembers, title='Members'),
		title =	'Members'
	))
	
	return oc