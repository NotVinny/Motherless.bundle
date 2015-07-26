from MLCommon import *

ML_VIDEO_SEARCH_URL =	BASE_URL + '/term/videos/'
ML_TERM_URL =			BASE_URL + '/term/videos/%s'

MAX_TERMS_PER_PAGE = 40

@route(ROUTE_PREFIX + '/tags')
def BrowseTags(title, url, page=1):

	oc = ObjectContainer(title2=title)
	
	oc.add(InputDirectoryObject(
		key =	Callback(SearchTags, title='Search Results'),
		title =	"Search Title",
		prompt =	"Search for...",
		summary =	"Enter Tag"
	))
	
	if (int(page) > 1):
		oc.add(DirectoryObject(
			key =	Callback(BrowseTags, title=title, url=url, page = int(page) - 1),
			title =	'Previous Page'
		))
	
	html = HTML.ElementFromURL(url)
	
	tags = html.xpath("//div[@id='content']/div/div[not(@class='header')]/a/@href")
	
	tagsSubSet = tags[MAX_TERMS_PER_PAGE * (int(page) - 1) : MAX_TERMS_PER_PAGE * int(page)]
	
	for tag in tagsSubSet:
		term =	tag.split('/')[-1]
		termURL =	ML_TERM_URL % term
		
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=term, url=termURL),
			title =	term
		))
	
	if (len(tags) >= MAX_TERMS_PER_PAGE * (int(page) - 1)):
		oc.add(DirectoryObject(
			key =	Callback(BrowseTags, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc

@route(ROUTE_PREFIX + '/tags/search')
def SearchTags(query, title):
	
	try:
		querySEND = String.StripTags(str(query))
		querySEND = querySEND.replace('%20',' ')
		querySEND = querySEND.replace('  ',' ')
		querySEND = querySEND.strip(' \t\n\r')
		querySEND = " ".join(querySEND.split())
		
		oc = ObjectContainer(title2 = title)
		
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title='Search Results', url=ML_VIDEO_SEARCH_URL + querySEND),
			title =	'Search Results'
		))
		return oc
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)