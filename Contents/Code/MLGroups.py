from MLCommon import *

ML_GROUPS_URL =			ML_BASE_URL + '/groups'
ML_GROUP_SEARCH_URL =		ML_GROUPS_URL + '/search?term=%s'
ML_GROUP_SORT_URL =		ML_GROUPS_URL + '?s=%s&c=%s'
ML_GROUP_VIDEO_URL =		ML_BASE_URL + '/gv/%s'

ML_MAX_GROUPS_PER_PAGE =	20

@route(ML_ROUTE_PREFIX + '/groups')
def BrowseGroups(title, url=ML_GROUPS_URL):
	
	# Create the object to contain all of the group categories
	oc = ObjectContainer(title2=title)
	
	# Add a search input
	oc.add(InputDirectoryObject(
		key =		Callback(SearchGroups, title='Search Results'),
		title =		"Search Groups",
		prompt =		"Search for...",
		summary =	"Enter Group Search Term"
	))
	
	# Get the HTML of the page
	html = HTML.ElementFromURL(url)
	
	# Use xPath to extract a list of group catgegories
	groupCategories = html.xpath("id('group-categories')/ul/li/a")
	
	# Loop through all group categories
	for groupCategory in groupCategories:
		# Get the group category text
		groupCategoryTitle = groupCategory.xpath("./text()")[0].strip()
		
		# Add a Directory Object for the group category
		oc.add(DirectoryObject(
			key =	Callback(SortGroups, title=groupCategoryTitle, groupCategory=groupCategoryTitle),
			title =	groupCategoryTitle
		))
	
	return oc

@route(ML_ROUTE_PREFIX + '/groups/search')
def SearchGroups(query, title):
	
	# Format the query for use in Motherless' search
	formattedQuery = formatStringForSearch(query, "+")
	
	try:
		return ListGroups(title='Search Results For: ' + query, url=ML_GROUP_SEARCH_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)

@route(ML_ROUTE_PREFIX + '/groups/sort')
def SortGroups(title, groupCategory):
	
	# Create the object to contain all of the sorting options
	oc = ObjectContainer(title2=title)
	
	# Create a dictionary of sort options
	sortOrders = OrderedDict([
		('All Groups',		'u'),
		('Most Uploads',	'n'),
		('Most Posts',		'f'),
		('Recently Created',	'r')
	])
	
	# Loop through all of the sort options
	for sortOrder, sortOrderFlag in sortOrders.items():
		# Create a Directory Object for the sort option
		oc.add(DirectoryObject(
			key =	Callback(ListGroups, title=groupCategory + ": " + sortOrder, url=ML_GROUP_SORT_URL % (sortOrderFlag, groupCategory)),
			title =	sortOrder
		))
	
	return oc

@route(ML_ROUTE_PREFIX + '/groups/list')
def ListGroups(title, url, page=1):
	
	#Create the object to contain all of the groups
	oc = ObjectContainer(title2=title)
	
	#Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get the HTML of the page
	html = HTML.ElementFromURL(pagedURL)
	
	# Use xPath to extract a list of groups
	groups = html.xpath("//div[@class='group-bio']")
	
	# Loop through all the groups
	for group in groups:
		# Get the details of the group
		groupURL =			ML_GROUP_VIDEO_URL % group.xpath("./h1/a/@href")[0].split('/')[-1]
		groupThumbnail =	group.xpath("./div[@class='group-bio-avatar']/a/div/img/@src")[0]
		groupTitle =		group.xpath("./h1/a/text()")[0].strip()
		
		# Add a Directory Object for the group
		oc.add(DirectoryObject(
			key =	Callback(ListVideos, title=groupTitle, url=groupURL),
			title =	groupTitle,
			thumb =	groupThumbnail
		))
	
	# There is a slight change that this will break... If the number of groups returned in total is divisible by ML_MAX_GROUPS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(groups) == ML_MAX_GROUPS_PER_PAGE):
		oc.add(NextPageObject(
			key =	Callback(ListGroups, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc