from MLCommon import *

ML_GROUPS_URL =			ML_BASE_URL + '/groups'
ML_GROUP_SEARCH_URL =		ML_GROUPS_URL + '/search?term=%s'
ML_GROUP_SORT_URL =		ML_GROUPS_URL + '?s=%s&c=%s'
ML_GROUP_VIDEO_URL =		ML_BASE_URL + '/gv/%s'

ML_MAX_GROUPS_PER_PAGE =	20

@route(ML_ROUTE_PREFIX + '/groups')
def BrowseGroups(title, url=ML_GROUPS_URL):
	
	# Create a dictionary of menu items
	browseGroupsMenuItems = OrderedDict([
		('Search Groups', {'function':SearchGroups, 'search':True, 'directoryObjectArgs':{'prompt':'Search for...','summary':"Enter Group Search Term"}})
	])
	
	# Get list of group categories
	groupCategories = SharedCodeService.MLGroups.GetGroupCategories(url)
	
	# Loop through all group categories
	for groupCategory in groupCategories:
		# Add a menu item for the group category
		browseGroupsMenuItems[groupCategory['title']] = {'function':SortGroups, 'functionArgs':{'groupCategory':groupCategory['title']}}
	
	return GenerateMenu(title, browseGroupsMenuItems)

@route(ML_ROUTE_PREFIX + '/groups/list')
def ListGroups(title, url, page=1):
	
	# Create a dictionary of menu items
	listGroupsMenuItems = OrderedDict()
	
	#Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get list of groups
	groups = SharedCodeService.MLGroups.GetGroups(pagedURL)
	
	# Loop through all the groups
	for group in groups:
		# Add a menu item for the group
		listGroupsMenuItems[group['title']] = {
			'function':				ListVideos,
			'functionArgs':			{'url': ML_GROUP_VIDEO_URL % group['url']},
			'directoryObjectArgs':	{'thumb': group['thumbnail']}
		}
	
	# There is a slight change that this will break... If the number of groups returned in total is divisible by ML_MAX_GROUPS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(groups) == ML_MAX_GROUPS_PER_PAGE):
		listGroupsMenuItems['Next Page'] = {'function':ListGroups, 'functionArgs':{'title':title, 'url':url, 'page':int(page)+1}, 'nextPage':True}
	
	return GenerateMenu(title, listGroupsMenuItems)

@route(ML_ROUTE_PREFIX + '/groups/search')
def SearchGroups(query):
	
	# Format the query for use in Motherless' search
	formattedQuery = formatStringForSearch(query, "+")
	
	try:
		return ListGroups(title='Search Results For: ' + query, url=ML_GROUP_SEARCH_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)

@route(ML_ROUTE_PREFIX + '/groups/sort')
def SortGroups(title, groupCategory):
	
	# Create a dictionary of menu items
	sortGroupsMenuItems = OrderedDict([
		('All Groups',		{'function':ListGroups, 'functionArgs':{'title':groupCategory + ' - All Groups',		'url':ML_GROUP_SORT_URL % ('u', groupCategory)}}),
		('Most Uploads',	{'function':ListGroups, 'functionArgs':{'title':groupCategory + ' - Most Uploads',		'url':ML_GROUP_SORT_URL % ('n', groupCategory)}}),
		('Most Posts',		{'function':ListGroups, 'functionArgs':{'title':groupCategory + ' - Most Posts',		'url':ML_GROUP_SORT_URL % ('f', groupCategory)}}),
		('Recently Created',	{'function':ListGroups, 'functionArgs':{'title':groupCategory + ' - Recently Created',	'url':ML_GROUP_SORT_URL % ('r', groupCategory)}})
	])
	
	return GenerateMenu(title, sortGroupsMenuItems)