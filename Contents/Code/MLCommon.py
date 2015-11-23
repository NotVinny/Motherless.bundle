import urllib
import urlparse

MAX_VIDEOS_PER_PAGE = 80

@route(ROUTE_PREFIX + '/list')
def ListVideos(title, url, page=1):
	
	# Create the object to contain all of the videos
	oc = ObjectContainer(title2 = title)
	
	# Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get the HTML of the site
	html = HTML.ElementFromURL(pagedURL)
	
	# Use xPath to extract a list of divs that contain videos
	videos = html.xpath("//div[@class='thumb video medium']")
	
	# Loop through the videos in the page
	for video in videos:
		# Get the link of the video
		videoURL = video.xpath("./a/@href")[0]
		
		# Check for relative URLs
		if (videoURL.startswith('/')):
			videoURL = BASE_URL + videoURL
		
		# Make sure the last step went smoothly (this is probably redundant but oh well)
		if (videoURL.startswith(BASE_URL)):
			# Get the video details
			thumbnail =	video.xpath("./a/img/@src")[0]
			videoTitle =	video.xpath("./div[@class='captions']/h2/text()")[0]
			
			# Create a Video Clip Object for the video
			vco = VideoClipObject(
				url =	videoURL,
				title =	videoTitle,
				thumb =	thumbnail
			)
			
			# Get the duration of the video
			durationString =	video.xpath("./div[@class='captions']/div[@class='caption left']/text()")[0]
			
			# Split it into a list separated by colon
			durationArray =	durationString.split(":")
			
			if (len(durationArray) == 2):
				# Dealing with MM:SS
				minutes =	int(durationArray[0])
				seconds =	int(durationArray[1])
				
				vco.duration = (minutes*60 + seconds) * 1000
				
			elif (len(durationArray) == 3):
				# Dealing with HH:MM:SS
				hours =		int(durationArray[0])
				minutes =	int(durationArray[1])
				seconds =	int(durationArray[2])
				
				vco.duration = (hours*3600 + minutes * 60 + seconds) * 1000
			else:
				# WTF
				pass
			
			# Add the Video Clip Object to the Object Container
			oc.add(vco)
	
	# There is a slight change that this will break... If the number of videos returned in total is divisible by MAX_VIDEOS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(videos) == MAX_VIDEOS_PER_PAGE):
		oc.add(NextPageObject(
			key =	Callback(ListVideos, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))

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