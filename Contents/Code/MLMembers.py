from MLCommon import *

ML_MEMBERS_URL =			ML_BASE_URL + '/members/verified'
ML_MEMBER_SEARCH_URL =		ML_BASE_URL + '/members/search?username=%s'
ML_MEMBER_GROUPS_URL =		ML_BASE_URL + '/groups/member/%s'
ML_MEMBER_FAVORITES_URL =	ML_BASE_URL + '/f/%s/videos'
ML_MEMBER_UPLOADS_URL =		ML_BASE_URL + '/u/%s?t=v'

ML_MAX_MEMBERS_PER_PAGE =	100

@route(ML_ROUTE_PREFIX + '/members')
def BrowseMembers(title, url=ML_MEMBERS_URL, page=1):
	
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
		memberURL =		ML_BASE_URL + member.xpath("./td[@class='thumb-member-info ellipsis']/div[@class='thumb-member-username']/a/@href")[0]
		memberThumbnail =	member.xpath("./td[@class='thumb-member-avatar']/a/img/@src")[0]
		
		# Add a Directory Object for the member
		oc.add(DirectoryObject(
			key =	Callback(MemberMenu, title=memberUsername, url=memberURL, username=memberUsername),
			title=		memberUsername,
			thumb =	memberThumbnail
		))
	
	# There is a slight change that this will break... If the number of members returned in total is divisible by ML_MAX_MEMBERS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(members) == ML_MAX_MEMBERS_PER_PAGE):
		oc.add(NextPageObject(
			key =	Callback(BrowseMembers, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc

@route(ML_ROUTE_PREFIX + '/members/menu')
def MemberMenu(title, url, username):
	
	# Create the object to contain all of the member options
	oc = ObjectContainer(title2=title)
	
	# TODO: Use some data structure to make this into a loop... A simple dictionary won't do, will need to ponder this. First change to be made for v1.3
	
	# Directory Object for Member's Favorites
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Favorites", url=ML_MEMBER_FAVORITES_URL % username),
		title =	'Favorites'
	))
	
	# Directory Object for Member's Uploads
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Uploads", url=ML_MEMBER_UPLOADS_URL % username),
		title =	'Uploads'
	))
	
	# Directory Object for Member's Groups
	oc.add(DirectoryObject(
		key =	Callback(ListGroups, title=username + "'s Groups", url=ML_MEMBER_GROUPS_URL % username),
		title =	'Groups'
	))
	
	return oc

@route(ML_ROUTE_PREFIX + '/members/search')
def SearchMembers(query, title):
	
	# Format the query for use in Motherless' search
	formattedQuery = formatStringForSearch(query, "+")
	
	try:
		return BrowseMembers(title='Search Results For: ' + query, url=ML_MEMBER_SEARCH_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)