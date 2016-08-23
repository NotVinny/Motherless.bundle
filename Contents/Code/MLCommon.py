import urllib
import urlparse
from collections import OrderedDict

ML_ROUTE_PREFIX =	'/video/motherless'

ML_BASE_URL =		'http://motherless.com'

ML_MAX_VIDEOS_PER_PAGE =	80

@route(ML_ROUTE_PREFIX + '/videos/browse')
def BrowseVideos(title):
	
	# Create a dictionary of menu items
	browseVideosMenuItems = OrderedDict([
		('Most Recent',				{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/recent'}}),
		('Most Viewed',				{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/viewed'}}),
		('Most Viewed - All Time',	{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/all/viewed'}}),
		('Most Favorited',			{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/favorited'}}),
		('Most Favorited - All Time',	{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/all/favorited'}}),
		('Most Commented',			{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/commented'}}),
		('Most Commented - All Time',	{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/all/commented'}}),
		('Popular',				{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/popular'}}),
		('Live',					{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/live/videos'}}),
		('Archives',				{'function':ListVideos, 'functionArgs':{'url':ML_BASE_URL + '/videos/archives'}}),
	])
	
	return GenerateMenu(title, browseVideosMenuItems)

@route(ML_ROUTE_PREFIX + '/videos/list')
def ListVideos(title, url, page=1):
	
	# Create the object to contain all of the videos
	oc = ObjectContainer(title2 = title)
	
	# Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get list of videos
	videos = SharedCodeService.MLCommon.GetVideos(pagedURL)
	
	# Loop through the videos in the page
	for video in videos:
		# Check for relative URLs
		if (video['url'].startswith('/')):
			video['url'] = ML_BASE_URL + video['url']
		
		# Make sure the last step went smoothly (this is probably redundant but oh well)
		if (video['url'].startswith(ML_BASE_URL)):
			
			# Add a Directory Object for the video to the Object Container
			oc.add(DirectoryObject(
				key =	Callback(VideoMenu, url=video["url"], title=video["title"], duration=video["duration"]),
				title =	video["title"],
				thumb =	video["thumbnail"],
				duration =	video["duration"]
			))
	
	# There is a slight change that this will break... If the number of videos returned in total is divisible by ML_MAX_VIDEOS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(videos) == ML_MAX_VIDEOS_PER_PAGE):
		oc.add(NextPageObject(
			key =	Callback(ListVideos, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))

	return oc

@route(ML_ROUTE_PREFIX + '/videos/menu')
def VideoMenu(url, title='Video Menu', duration=0):
	# Create the object to contain all of the videos options
	oc = ObjectContainer(title2 = title, no_cache=True)
	
	# Create the Video Clip Object
	vco =	URLService.MetadataObjectForURL(url)
	
	# As I am calling MetadataObjectForURL from the URL Service, it only returns the metadata, it doesn't contain the URL
	vco.url =	url
	
	# Overide the title
	vco.title =	"Play Video"
	
	if (int(duration) > 0):
		vco.duration = int(duration)
	
	# Add the Video Clip Object
	oc.add(vco)
	
	# Get the HTML of the site
	html =		HTML.ElementFromURL(url)
	
	# Use xPath to extract the videoID
	videoID = html.xpath("//input[@name='codename']/@value")
	
	if (len(videoID) > 0):
		videoID =	videoID[0]
		
		videoThumbnailTileURL = SharedCodeService.MLCommon.GetVideoThumbnails(videoID)
		
		oc.add(PhotoObject(
			key =			videoThumbnailTileURL,
			rating_key =	videoThumbnailTileURL,
			title =			"Tiled Thumbnails",
			thumb =			videoThumbnailTileURL
		))
	
	return oc

def GenerateMenu(title, menuItems, no_cache=False):
	# Create the object to contain the menu items
	oc = ObjectContainer(title2=title, no_cache=no_cache)
	
	# Loop through the menuItems dictionary
	for menuTitle, menuData in menuItems.items():
		# Create empty dictionaries to hold the arguments for the Directory Object and the Function
		directoryObjectArgs =	{}
		functionArgs =		{}
		
		# See if any Directory Object arguments are present in the menu data
		if ('directoryObjectArgs' in menuData):
			# Merge dictionaries
			directoryObjectArgs.update(menuData['directoryObjectArgs'])
		
		# Check to see if the menu item is a search menu item
		if ('search' in menuData and menuData['search'] == True):
			directoryObject = InputDirectoryObject(title=menuTitle, **directoryObjectArgs)
		# Check to see if the menu item is a next page item
		elif ('nextPage' in menuData and menuData['nextPage'] == True):
			directoryObject = NextPageObject(title=menuTitle, **directoryObjectArgs)
		# Otherwise, use a basic Directory Object
		else:
			directoryObject = DirectoryObject(title=menuTitle, **directoryObjectArgs)
			functionArgs['title'] = menuTitle
		
		# See if any Function arguments are present in the menu data
		if ('functionArgs' in menuData):
			# Merge dictionaries
			functionArgs.update(menuData['functionArgs'])
		
		# Set the Directory Object key to the function from the menu data, passing along any additional function arguments
		directoryObject.key =	Callback(menuData['function'], **functionArgs)
		
		# Add the Directory Object to the Object Container
		oc.add(directoryObject)
	
	return oc

# I stole this function from http://stackoverflow.com/questions/2506379/add-params-to-given-url-in-python. It works.
def addURLParamaters (url, params):
	
	urlParts =	list(urlparse.urlparse(url))
	
	urlQuery =	dict(urlparse.parse_qsl(urlParts[4]))
	urlQuery.update(params)

	urlParts[4] = urllib.urlencode(urlQuery)

	return urlparse.urlunparse(urlParts)

# I stole this function (and everything I did for search basically) from the RedTube Plex Plugin, this file specifically https://github.com/flownex/RedTube.bundle/blob/master/Contents/Code/PCbfSearch.py
def formatStringForSearch(query, delimiter):
	query = String.StripTags(str(query))
	query = query.replace('%20',' ')
	query = query.replace('  ',' ')
	query = query.strip(' \t\n\r')
	query = delimiter.join(query.split())
	
	return query