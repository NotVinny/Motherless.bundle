from MLCommon import *

MEMBER_SEARCH_URL =		BASE_URL + '/members/search'
MEMBER_GROUPS_URL =	BASE_URL + '/groups/member/%s'
MEMBER_FAVORITES_URL =	BASE_URL + '/f/%s/videos'
MEMBER_UPLOADS_URL =	BASE_URL + '/u/%s?t=v'

MAX_MEMBERS_PER_PAGE =	100

@route(ROUTE_PREFIX + '/members')
def BrowseMembers(title, url, page=1):
	
	# Create the object to contain all of the members
	oc = ObjectContainer(title2=title)
	
	# Add a search input to the first page
	if (int(page) == 1):
		oc.add(InputDirectoryObject(
			key =		Callback(SearchMembers, title='Search Members'),
			prompt =		"Search for...",
			title =		"Search Members",
			summary =	"Enter Tag"
		))
	
	# Add the page number into the query string
	pagedURL = addURLParamaters(url, {'page':str(page)})
	
	# Get the HTML of the page
	html = HTML.ElementFromURL(pagedURL)
	
	# Use xPath to extract a list of members
	members = html.xpath("//table[@class='thumbs-members']//tr")
	
	# Loop through all the members
	for member in members:
		# Get the member details
		memberUsername =	member.xpath("./td[@class='thumb-member-info ellipsis']/div[@class='thumb-member-username']/a/text()")[0].strip()
		memberURL =			BASE_URL + member.xpath("./td[@class='thumb-member-info ellipsis']/div[@class='thumb-member-username']/a/@href")[0]
		memberThumbnail =	member.xpath("./td[@class='thumb-member-avatar']/a/img/@src")[0]
		
		# Add a Directory Object for the member
		oc.add(DirectoryObject(
			key =	Callback(MemberMenu, title=memberUsername, url=memberURL, username=memberUsername),
			title=	memberUsername,
			thumb =	memberThumbnail
		))
	
	# There is a slight change that this will break... If the number of members returned in total is divisible by MAX_MEMBERS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(members) == MAX_MEMBERS_PER_PAGE):
		oc.add(NextPageObject(
			key =	Callback(BrowseMembers, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc

@route(ROUTE_PREFIX + '/members/menu')
def MemberMenu(title, url, username):
	
	# Create the object to contain all of the member options
	oc = ObjectContainer(title2=title)
	
	# Directory Object for Member's Favorites
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Favorites", url=MEMBER_FAVORITES_URL % username),
		title =	'Favorites'
	))
	
	# Directory Object for Member's Uploads
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Uploads", url=MEMBER_UPLOADS_URL % username),
		title =	'Uploads'
	))
	
	# Directory Object for Member's Groups
	oc.add(DirectoryObject(
		key =	Callback(ListGroups, title=username + "'s Groups", url=MEMBER_GROUPS_URL % username),
		title =	'Groups'
	))
	
	return oc

@route(ROUTE_PREFIX + '/members/search')
def SearchMembers(query, title):
	
	# Format the query for use in Motherless' search
	query = formatStringForSearch(query, "+")
	
	try:
		# Create a page that only has one Directory Object, Search Results... There must be a way to bypass this, but I sure as hell don't know it
		oc = ObjectContainer(title2 = title)
		
		# Create the search results Directory Object
		oc.add(DirectoryObject(
			key =	Callback(BrowseMembers, title='Search Results', url=MEMBER_SEARCH_URL + '?username=' + query),
			title =	'Search Results'
		))
		return oc
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)