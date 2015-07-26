import urllib
import urlparse

MAX_VIDEOS_PER_PAGE = 80

@route(ROUTE_PREFIX + '/list')
def ListVideos(title, url, page=1):
	
	params = {'page':str(page)}
	
	urlParts =	list(urlparse.urlparse(url))
	urlQuery =	dict(urlparse.parse_qsl(urlParts[4]))
	urlQuery.update(params)

	urlParts[4] = urllib.urlencode(urlQuery)

	pagedURL = urlparse.urlunparse(urlParts)
	
	oc = ObjectContainer(title2=title)
	
	if (int(page) > 1):
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=title, url=url, page = int(page) - 1),
			title =	'Previous Page'
		))

	html = HTML.ElementFromURL(pagedURL)

	videos = html.xpath("//div[@class='thumb video medium']")
	
	for video in videos:
		videoURL = video.xpath("./a/@href")[0]
		if (videoURL.startswith('/')):
			videoURL = BASE_URL + videoURL
		
		if (videoURL.startswith(BASE_URL)):
			thumbnail =	video.xpath("./a/img/@src")[0]
			videoTitle =	video.xpath("./div[@class='captions']/h2/text()")[0]
			
			oc.add(VideoClipObject(
				url =		videoURL,
				title =	videoTitle,
				thumb =	thumbnail
			))
	
	if (len(videos) == MAX_VIDEOS_PER_PAGE):
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))

	return oc