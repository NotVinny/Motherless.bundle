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
	
	oc = ObjectContainer(title2=title)
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Recent', url=MOST_RECENT_URL),
		title =	'Most Recent'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Viewed', url=MOST_VIEWED_URL),
		title =	'Most Viewed'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Viewed All Time', url=MOST_VIEWED_ALL_TIME_URL),
		title =	'Most Viewed All Time'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Favorited', url=MOST_FAVORITED_URL),
		title =	'Most Favorited'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Favorited All Time', url=MOST_FAVORITED_ALL_TIME_URL),
		title =	'Most Favorited All Time'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Commented', url=MOST_COMMENTED_URL),
		title =	'Most Commented'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Most Commented All Time', url=MOST_COMMENTED_ALL_TIME_URL),
		title =	'Most Commented All Time'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Popular', url=POPULAR_URL),
		title =	'Popular'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Live', url=LIVE_URL),
		title =	'Live'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title='Archives', url=ARCHIVES_URL),
		title =	'Archives'
	))
	
	return oc