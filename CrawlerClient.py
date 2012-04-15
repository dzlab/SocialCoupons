# citySelectBox to crawl cities (and corresponding url) where groupon operates in
# itemsLocalDeals to crawl local deals of a given city
# itemsShoppingDeals to crawl shipping deals (they do not depend on cities)
# itemsTravelDeals to crawl travel deals (they do not depend on cities)
import urllib2
import json
import httplib, urllib
#from bs4 import BeautifulSoup

#page = urllib2.urlopen("http://www.groupon.fr/all-deals/paris")
page = urllib2.urlopen("http://www.groupon.fr/all-deals/tarbes")
#soup = BeautifulSoup(page)
html = page.read()
stBracket = html.find('[', html.find('itemsLocalDeals = '))
ndBracket = html.find(']', stBracket)
localDeals = html[stBracket: ndBracket+1]
deals = json.loads(localDeals)

print jstr[0]['category']
print 'http://www.groupon.fr' + jstr[0]['dealPermaLink']
print jstr[0]['dealPrice']
print jstr[0]['imageUrl']
print jstr[0]['dealTitleTruncated']
print jstr[0]['cityUrlName']
print jstr[0]['dealTitle']
print jstr[0]['dealId']
print jstr[0]['dealOldPrice']
"""
index = {}
def filter_keyword(keyword):
	blacklist = ['ces','sans', 'all', 'eux', 'pas', 'une', 'vos', 'des', 'avec', 'ses', 'ces', ]
	if len(keyword)<3 or keyword.lower() in blacklist:
		return False
	if keyword.isalpha():
		return True
	return False

for d in deals:
	link = 'http://www.groupon.fr' + d['dealPermaLink']
	keywords = d['dealTitle'].split()
	for keyword in keywords:
		if filter_keyword(keyword):
			if keyword in index:
				index[keyword.lower()].append([link, 0])
			else:
				index[keyword.lower()] = [[link, 0]]
"""
params = urllib.urlencode({'deals': localDeals})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost:8080")
conn.request("POST", "/manage", params, headers)
response = conn.getresponse()
print response.status, response.reason

data = response.read()
data

conn.close()

#f = open('C:\\Dev\\udacity\\deal_jsonarray.txt', 'rb')
#tmp = f.read()
#deals = json.loads(tmp)