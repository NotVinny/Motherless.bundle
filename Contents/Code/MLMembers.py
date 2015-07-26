from MLCommon import *

MEMBER_SEARCH_URL =	BASE_URL + '/members/search'
MEMBER_GROUPS_URL =	BASE_URL + '/groups/member/%s'
MEMBER_FAVORITES_URL =	BASE_URL + '/f/%s/videos'
MEMBER_UPLOADS_URL =	BASE_URL + '/u/%s?t=v'

MAX_MEMBERS_PER_PAGE =	100

@route(ROUTE_PREFIX + '/members')
def BrowseMembers(title, url, page=1):
	
	params = {'page':str(page)}
	
	urlParts =	list(urlparse.urlparse(url))
	urlQuery =	dict(urlparse.parse_qsl(urlParts[4]))
	urlQuery.update(params)

	urlParts[4] = urllib.urlencode(urlQuery)

	pagedURL = urlparse.urlunparse(urlParts)
	
	oc = ObjectContainer(title2=title)
	
	if (int(page) > 1):
		oc.add(DirectoryObject(
			key =	Callback(BrowseMembers, title=title, url=url, page = int(page) - 1),
			title =	'Previous Page'
		))
	
	oc.add(InputDirectoryObject(
		key =	Callback(SearchMembers, title='Search Members'),
		prompt =	"Search for...",
		title =	"Search Members",
		summary =	"Enter Tag"
	))
	
	html = HTML.ElementFromURL(pagedURL)
	
	members = html.xpath("//table[@class='thumbs-members']//tr")
	
	for member in members:
		memberUsername =	member.xpath("./td[@class='thumb-member-info ellipsis']/div[@class='thumb-member-username']/a/text()")[0].strip()
		memberURL =		BASE_URL + member.xpath("./td[@class='thumb-member-info ellipsis']/div[@class='thumb-member-username']/a/@href")[0]
		memberThumbnail =	member.xpath("./td[@class='thumb-member-avatar']/a/img/@src")[0]
		
		oc.add(DirectoryObject(
			key =	Callback(MemberMenu, title=memberUsername, url=memberURL, username=memberUsername),
			title=		memberUsername,
			thumb =	memberThumbnail
		))
	
	if (len(members) == MAX_MEMBERS_PER_PAGE):
		oc.add(DirectoryObject(
			key =	Callback(BrowseMembers, title=title, url=url, page = int(page)+1),
			title =	'Next Page'
		))
	
	return oc

@route(ROUTE_PREFIX + '/members/menu')
def MemberMenu(title, url, username):
	
	oc = ObjectContainer(title2=title)
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Favorites", url=MEMBER_FAVORITES_URL % username),
		title =	'Favorites'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListVideos, title=username + "'s Uploads", url=MEMBER_UPLOADS_URL % username),
		title =	'Uploads'
	))
	
	oc.add(DirectoryObject(
		key =	Callback(ListGroups, title=username + "'s Groups", url=MEMBER_GROUPS_URL % username),
		title =	'Groups'
	))
	
	return oc

@route(ROUTE_PREFIX + '/members/search')
def SearchMembers(query, title):
	
	try:
		querySEND = String.StripTags(str(query))
		querySEND = querySEND.replace('%20','+')
		querySEND = querySEND.replace('  ','+')
		querySEND = querySEND.strip(' \t\n\r')
		querySEND = " ".join(querySEND.split())
		
		oc = ObjectContainer(title2 = title)
		
		oc.add(DirectoryObject(
			key =	Callback(BrowseMembers, title='Search Results', url=MEMBER_SEARCH_URL + '?username=' + querySEND),
			title =	'Search Results'
		))
		return oc
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)