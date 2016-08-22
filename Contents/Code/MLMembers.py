from MLCommon import *

ML_MEMBERS_URL =			ML_BASE_URL + '/members'
ML_MEMBER_SEARCH_URL =		ML_MEMBERS_URL + '/search?username=%s'
ML_MEMBER_GROUPS_URL =		ML_BASE_URL + '/groups/member/%s'
ML_MEMBER_FAVORITES_URL =	ML_BASE_URL + '/f/%s/videos'
ML_MEMBER_UPLOADS_URL =		ML_BASE_URL + '/u/%s?t=v'

ML_MAX_MEMBERS_PER_PAGE =	100

@route(ML_ROUTE_PREFIX + '/members')
def BrowseMembers(title):
	
	# Create a dictionary of menu items
	browseMembersMenuItems = OrderedDict([
		('Search Members',	{'function':SearchMembers, 'search':True, 'directoryObjectArgs':{'prompt':'Search for...','summary':"Enter Member Search Term"}}),
		('Top Uploaders',	{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/uploader'}}),
		('Top Viewed',		{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/viewed'}}),
		('Top Social',		{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/social'}}),
		('Top Favorited',	{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/favorited'}}),
		('Top Commented',	{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/commented'}}),
		('Top Mentioned',	{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/top/mentioned'}}),
		('Gender Verified',	{'function':ListMembers, 'functionArgs':{'url':ML_MEMBERS_URL + '/verified'}})
	])
	
	return GenerateMenu(title, browseMembersMenuItems)

@route(ML_ROUTE_PREFIX + '/members/list')
def ListMembers(title, url=ML_MEMBERS_URL, page=1):
	
	# Create a dictionary of menu items
	listMembersMenuItems = OrderedDict()
	
	# Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get list of members
	members = SharedCodeService.MLMembers.GetMembers(pagedURL)
	
	# Loop through all the members
	for member in members:
		# Add a menu item for the member
		listMembersMenuItems[member['username']] = {
			'function':				MemberMenu,
			'functionArgs':			{'url':ML_BASE_URL + member['url'],'username':member['username']},
			'directoryObjectArgs':	{'thumb':member['thumbnail']}
		}
	
	# There is a slight change that this will break... If the number of members returned in total is divisible by ML_MAX_MEMBERS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(members) == ML_MAX_MEMBERS_PER_PAGE):
		listMembersMenuItems['Next Page'] = {'function':ListMembers, 'functionArgs':{'title':title, 'url':url, 'page':int(page)+1}, 'nextPage':True}
	
	return GenerateMenu(title, listMembersMenuItems)

@route(ML_ROUTE_PREFIX + '/members/search')
def SearchMembers(query):
	
	# Format the query for use in Motherless' search
	formattedQuery = formatStringForSearch(query, "+")
	
	try:
		return ListMembers(title='Search Results For: ' + query, url=ML_MEMBER_SEARCH_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)

@route(ML_ROUTE_PREFIX + '/members/menu')
def MemberMenu(title, url, username):
	
	# Create a dictionary of menu items
	memberMenuItems = OrderedDict([
		('Favorites',	{'function':ListVideos, 'functionArgs':{'title':username + "'s Favorites", 'url':ML_MEMBER_FAVORITES_URL % username}}),
		('Uploads',	{'function':ListVideos, 'functionArgs':{'title':username + "'s Uploads", 'url':ML_MEMBER_UPLOADS_URL % username}}),
		('Groups',		{'function':ListGroups, 'functionArgs':{'title':username + "'s Groups", 'url':ML_MEMBER_GROUPS_URL % username}})
	])
	
	return GenerateMenu(title, memberMenuItems)