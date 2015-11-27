from MLCommon import *

ML_SEARCH_TAGS_URL =		ML_BASE_URL + '/search/cloud'
ML_TERM_URL =				ML_BASE_URL + '/term/videos/%s'

ML_MAX_TERMS_PER_PAGE =	50

@route(ML_ROUTE_PREFIX + '/tags/list')
def ListTags(title, url=ML_SEARCH_TAGS_URL, page=1):
	
	# Create a dictionary of menu items
	listTagsMenuItems = OrderedDict()
	
	# Get the HTML of the site
	html = HTML.ElementFromURL(url)
	
	# Use xPath to extract a list of tags
	tags = html.xpath("//div[@id='content']/div/div[not(@class='header')]/a/@href")
	
	# Get a subset of the tags based on the page number
	tagsSubSet = tags[ML_MAX_TERMS_PER_PAGE * (int(page) - 1) : ML_MAX_TERMS_PER_PAGE * int(page)]
	
	# Loop through all tags
	for tag in tagsSubSet:
		# Get the term text
		term =		tag.split('/')[-1]
		
		# Add a menu item for the tag
		listTagsMenuItems[term] = {'function':ListVideos, 'functionArgs':{'url':ML_TERM_URL % term}}
	
	# There is a slight change that this will break... If the number of tags returned in total is divisible by ML_MAX_TERMS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(tags) >= ML_MAX_TERMS_PER_PAGE * (int(page) - 1)):
		listTagsMenuItems['Next Page'] = {'function':ListTags, 'functionArgs':{'title':title, 'url':url, 'page':int(page)+1}, 'nextPage':True}
	
	return GenerateMenu(title, listTagsMenuItems)

@route(ML_ROUTE_PREFIX + '/tags/search')
def SearchTags(query):
	
	# Format the query for use in Motherless' search
	formattedQuery = formatStringForSearch(query, "+")
	
	try:
		return ListVideos(title='Search Results For: ' + query, url=ML_TERM_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)