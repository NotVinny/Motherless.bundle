from MLCommon import *

ML_TERM_URL =			BASE_URL + '/term/videos/%s'
MAX_TERMS_PER_PAGE =	40

@route(ROUTE_PREFIX + '/tags')
def BrowseTags(title, url, page=1):
	
	# Create the object to contain all of the tags
	oc = ObjectContainer(title2=title)
	
	# Add a search input to the first page
	if (int(page) == 1):
		oc.add(InputDirectoryObject(
			key =		Callback(SearchTags, title='Search Results'),
			title =		"Search Title",
			prompt =		"Search for...",
			summary =	"Enter Tag"
		))
	
	# Get the HTML of the site
	html = HTML.ElementFromURL(url)
	
	# Use xPath to extract a list of tags
	tags = html.xpath("//div[@id='content']/div/div[not(@class='header')]/a/@href")
	
	# Get a subset of the tags based on the page number
	tagsSubSet = tags[MAX_TERMS_PER_PAGE * (int(page) - 1) : MAX_TERMS_PER_PAGE * int(page)]
	
	# Loop through all tags
	for tag in tagsSubSet:
		# Get the term text
		term =		tag.split('/')[-1]
		
		# Add a Directory Object that points to the search results for the term
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=term, url=ML_TERM_URL % term),
			title =	term
		))
	
	# There is a slight change that this will break... If the number of tags returned in total is divisible by MAX_TERMS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(tags) >= MAX_TERMS_PER_PAGE * (int(page) - 1)):
		oc.add(NextPageObject(
			key =	Callback(BrowseTags, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc

@route(ROUTE_PREFIX + '/tags/search')
def SearchTags(query, title):
	
	# Format the query for use in Motherless' search
	query = formatStringForSearch(query, "+")
	
	try:
		# Create a page that only has one Directory Object, Search Results... There must be a way to bypass this, but I sure as hell don't know it
		oc = ObjectContainer(title2 = title)
		
		# Create the search results Directory Object
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title='Search Results', url=ML_TERM_URL % query),
			title =	'Search Results'
		))
		return oc
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)