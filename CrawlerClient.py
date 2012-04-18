# citySelectBox to crawl cities (and corresponding url) where groupon operates in
# itemsLocalDeals to crawl local deals of a given city
# itemsShoppingDeals to crawl shipping deals (they do not depend on cities)
# itemsTravelDeals to crawl travel deals (they do not depend on cities)
import urllib2
import json
import httplib, urllib

# upload crawled deals to the web server
def upload(url, deals):
	params = urllib.urlencode({'deals': deals})
	headers = {"Content-type": "application/x-www-form-urlencoded",
    	       "Accept": "text/plain"}
	conn = httplib.HTTPConnection(url)
	conn.request("POST", "/manage", params, headers)
	response = conn.getresponse()
	print response.status, response.reason
	data = response.read()
	print 'Server response: ' + data
	conn.close()
	
# crawl local deals for a given city
def crawlLocalDeals(url):
	page = urllib2.urlopen(url)
	html = page.read()
	stBracket = html.find('[', html.find('itemsLocalDeals = '))
	ndBracket = html.find(']', stBracket)
	content = html[stBracket: ndBracket+1]
	return content

#page = urllib2.urlopen("http://www.groupon.fr/all-deals/paris")

# crawl all cities where we can find groupon local deals
def crawlCities():
	cities = {}
	page = urllib2.urlopen("http://www.groupon.fr/")
	html = page.read()
	start = html.find('<ul id="jCitiesSelectBox">')
	end = html.find('</ul>', start)
	while start < end:
		stQuote = html.find('\'', start)
		if stQuote > end:
			break
		ndQuote = html.find('\'', stQuote+1)
		url = html[stQuote+1:ndQuote]
		stSpan = html.find('<span>', ndQuote)
		ndSpan = html.find('</span>', ndQuote)
		offset = len('<span>')
		city = html[stSpan+offset:ndSpan]
		cities[city] = url
		start = html.find('</li>', start+1)
	return cities

# main code
# crawl cities, then for each one crawl its local deals and upload them to the server
number = 0
cities = crawlCities()
for city in cities:
	number = number + 1
	url = cities[city]
	url = url.replace('deals', 'all-deals')
	localDeals = crawlLocalDeals(url)
	upload("localhost:8080", localDeals)
	print 'Uploading local deals for ' + city + ' ('+str(number)+' of '+str(len(cities))+' cities) ... DONE'
