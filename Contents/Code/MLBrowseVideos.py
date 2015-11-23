from MLCommon import *

MOST_RECENT_URL =				BASE_URL + '/videos/recent'
MOST_VIEWED_URL =				BASE_URL + '/videos/viewed'
MOST_VIEWED_ALL_TIME_URL =		BASE_URL + '/videos/all/viewed'
MOST_FAVORITED_URL =			BASE_URL + '/videos/favorited'
MOST_FAVORITED_ALL_TIME_URL =	BASE_URL + '/videos/all/favorited'
MOST_COMMENTED_URL =			BASE_URL + '/videos/commented'
MOST_COMMENTED_ALL_TIME_URL =	BASE_URL + '/videos/all/commented'
POPULAR_URL =					BASE_URL + '/videos/popular'
LIVE_URL =						BASE_URL + '/live/videos'
ARCHIVES_URL =					BASE_URL + '/videos/archives'

@route(ROUTE_PREFIX + '/browse')
def BrowseVideos(title):
	
	# Create the object to contain the menu
	oc = ObjectContainer(title2=title)
	
	# Directory Object for Most Recent
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Recent', url=MOST_RECENT_URL),
		title =	'Most Recent'
	))
	
	# Directory Object for Most Viewed
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Viewed', url=MOST_VIEWED_URL),
		title =	'Most Viewed'
	))
	
	# Directory Object for Most Viewed - All Time
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Viewed - All Time', url=MOST_VIEWED_ALL_TIME_URL),
		title =	'Most Viewed - All Time'
	))
	
	# Directory Object for Most Favorited
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Favorited', url=MOST_FAVORITED_URL),
		title =	'Most Favorited'
	))
	
	# Directory Object for Most Favorited - All Time
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Favorited - All Time', url=MOST_FAVORITED_ALL_TIME_URL),
		title =	'Most Favorited - All Time'
	))
	
	# Directory Object for Most Commented
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Commented', url=MOST_COMMENTED_URL),
		title =	'Most Commented'
	))
	
	# Directory Object for Most Commented - All Time
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Commented - All Time', url=MOST_COMMENTED_ALL_TIME_URL),
		title =	'Most Commented - All Time'
	))
	
	# Directory Object for Popular
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Popular', url=POPULAR_URL),
		title =	'Popular'
	))
	
	# Directory Object for Live
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Live', url=LIVE_URL),
		title =	'Live'
	))
	
	# Directory Object for Archives
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Archives', url=ARCHIVES_URL),
		title =	'Archives'
	))
	
	return oc