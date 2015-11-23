NAME =				'Motherless'

BASE_URL =			'http://motherless.com'
GROUPS_URL =		BASE_URL + '/groups'
SEARCH_TAGS_URL =	BASE_URL + '/search/cloud'
MEMBERS_URL =		BASE_URL + '/members/verified'

ROUTE_PREFIX =		'/video/motherless'

ART =				'art-default.jpg'
ICON =				'icon-default.jpg'

from MLCommon import *
from MLBrowseVideos import *
from MLGroups import *
from MLTags import *
from MLMembers import *

def Start():
	
	# Set the defaults for Object Containers
	ObjectContainer.art =	R(ART)
	ObjectContainer.title1 =	NAME
	
	# Set the defaults of Directory Objects
	DirectoryObject.thumb =	R(ICON)
	
	# Set the cache lifespan
	HTTP.CacheTime = CACHE_1HOUR * 2
	
	# Set the user agent
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.3 (KHTML, like Gecko) Version/8.0.1 Safari/600.2.3'

@handler(ROUTE_PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():
	
	# Create the object to contain the main menu options
	oc = ObjectContainer()
	
	# Directory Object for Browse All Videos
	oc.add(DirectoryObject(
		key =	Callback(BrowseVideos, title='Browse All Videos'),
		title =	'Browse All Videos'
	))
	
	# Directory Object for Groups
	oc.add(DirectoryObject(
		key =	Callback(BrowseGroups, title='Groups', url=GROUPS_URL),
		title =	'Groups'
	))
	
	# Directory Object for Tags
	oc.add(DirectoryObject(
		key =	Callback(BrowseTags, title='Tags', url=SEARCH_TAGS_URL),
		title =	'Tags'
	))
	
	# Directory Object for Members
	oc.add(DirectoryObject(
		key =	Callback(BrowseMembers, title='Members', url=MEMBERS_URL),
		title =	'Members'
	))
	
	return oc