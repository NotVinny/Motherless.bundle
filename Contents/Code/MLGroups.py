from MLCommon import *

ML_GROUP_SEARCH_URL =	BASE_URL + '/groups/search?term='
ML_GROUP_SORT_URL =	BASE_URL + '/groups?s=%s&c=%s'
ML_GROUP_VIDEO_URL =	BASE_URL + '/gv/%s'

MAX_GROUPS_PER_PAGE = 20

@route(ROUTE_PREFIX + '/groups')
def BrowseGroups(title, url):
	
	oc = ObjectContainer(title2=title)
	
	oc.add(InputDirectoryObject(
		key =	Callback(SearchGroups, title='Search Results'),
		title =	"Search Groups",
		prompt =	"Search for...",
		summary =	"Enter Group Search Term"
	))
	
	html = HTML.ElementFromURL(url)
	
	groupCategories = html.xpath("id('group-categories')/ul/li/a")
	
	for groupCategory in groupCategories:
		groupCategoryTitle = groupCategory.xpath("./text()")[0].strip()
		
		oc.add(DirectoryObject(
			key =	Callback(SortGroups, title=groupCategoryTitle, groupCategory=groupCategoryTitle),
			title =	groupCategoryTitle
		))
	
	return oc

@route(ROUTE_PREFIX + '/groups/search')
def SearchGroups(query, title):
	
	try:
		querySEND = String.StripTags(str(query))
		querySEND = querySEND.replace('%20','+')
		querySEND = querySEND.replace('  ','+')
		querySEND = querySEND.strip(' \t\n\r')
		querySEND = " ".join(querySEND.split())
		
		oc = ObjectContainer(title2 = title)
		
		oc.add(DirectoryObject(
			key =	Callback(ListGroups, title='Search Results', url=ML_GROUP_SEARCH_URL + querySEND),
			title =	'Search Results'
		))
		
		return oc
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)

@route(ROUTE_PREFIX + '/groups/sort')
def SortGroups(title, groupCategory):
	oc = ObjectContainer(title2=title)
	
	sortOptionsDictionary = {'u' : 'All Groups', 'n' :  'Most Uploads',  'f' : 'Most Posts', 'r' : 'Recently Created'}
	
	for key, value in sortOptionsDictionary.iteritems():
		
		url = ML_GROUP_SORT_URL % (key, groupCategory)
		
		oc.add(DirectoryObject(
			key =	Callback(ListGroups, title=groupCategory, url=url),
			title =	value
		))
	
	return oc

@route(ROUTE_PREFIX + '/groups/list')
def ListGroups(title, url, page=1):
	
	params = {'page':str(page)}
	
	urlParts =	list(urlparse.urlparse(url))
	urlQuery =	dict(urlparse.parse_qsl(urlParts[4]))
	urlQuery.update(params)

	urlParts[4] = urllib.urlencode(urlQuery)

	pagedURL = urlparse.urlunparse(urlParts)
	
	oc = ObjectContainer(title2=title)
	
	if (int(page) > 1):
		oc.add(DirectoryObject(
			key =	Callback(ListGroups, title=title, url=url, page = int(page) - 1),
			title =	'Previous Page'
		))
	
	html = HTML.ElementFromURL(pagedURL)
	
	groups = html.xpath("//div[@class='group-bio']")
	
	for group in groups:
		groupURL =			ML_GROUP_VIDEO_URL % group.xpath("./h1/a/@href")[0].split('/')[-1]
		groupThumbnail =	group.xpath("./div[@class='group-bio-avatar']/a/div/img/@src")[0]
		groupTitle =		group.xpath("./h1/a/text()")[0].strip()
		
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=groupTitle, url=groupURL),
			title =	groupTitle,
			thumb =	groupThumbnail
		))
	
	if (len(groups) == MAX_GROUPS_PER_PAGE):
		oc.add(DirectoryObject(
			key =	Callback(ListGroups, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc