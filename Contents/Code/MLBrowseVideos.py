from MLCommon import *

ML_MOST_RECENT_URL =			ML_BASE_URL + '/videos/recent'
ML_MOST_VIEWED_URL =			ML_BASE_URL + '/videos/viewed'
ML_MOST_VIEWED_ALL_TIME_URL =	ML_BASE_URL + '/videos/all/viewed'
ML_MOST_FAVORITED_URL =			ML_BASE_URL + '/videos/favorited'
ML_MOST_FAVORITED_ALL_TIME_URL =	ML_BASE_URL + '/videos/all/favorited'
ML_MOST_COMMENTED_URL =		ML_BASE_URL + '/videos/commented'
ML_MOST_COMMENTED_ALL_TIME_URL =	ML_BASE_URL + '/videos/all/commented'
ML_POPULAR_URL =				ML_BASE_URL + '/videos/popular'
ML_LIVE_URL =					ML_BASE_URL + '/live/videos'
ML_ARCHIVES_URL =				ML_BASE_URL + '/videos/archives'

@route(ML_ROUTE_PREFIX + '/browse')
def BrowseVideos(title):
	
	# Create the object to contain the menu
	oc = ObjectContainer(title2=title)
	
	# Create a dictionary of all of the possible sort options and their URLs
	sortOrders = OrderedDict([
		('Most Recent',				ML_MOST_RECENT_URL),
		('Most Viewed',				ML_MOST_VIEWED_URL),
		('Most Viewed - All Time',	ML_MOST_VIEWED_ALL_TIME_URL),
		('Most Favorited',			ML_MOST_FAVORITED_URL),
		('Most Favorited - All Time',	ML_MOST_FAVORITED_ALL_TIME_URL),
		('Most Commented',			ML_MOST_COMMENTED_URL),
		('Most Commented - All Time',	ML_MOST_COMMENTED_ALL_TIME_URL),
		('Popular',				ML_POPULAR_URL),
		('Live',					ML_LIVE_URL),
		('Archives',				ML_ARCHIVES_URL)
	])
	
	# Loop through all of the sort orders
	for sortOrder, sortURL in sortOrders.items():
		# Add a Directory Object for the sort order
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=sortOrder, url=sortURL),
			title =	sortOrder
		))
	
	return oc