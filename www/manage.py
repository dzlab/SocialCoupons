from google.appengine.ext import webapp
from www.models.deal import *

import json

class Manager(webapp.RequestHandler):    
    def get(self):
        response = ''
        deals = Deal.all().fetch(1000)
        for deal in deals:
            response = response + deal.category + '- '+ deal.title + '\n'            
        #db.delete(Deal.all().fetch(1000))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(response)
        
    def post(self):
        if not self.request.get('deals'):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Deals parameter is missing in received request')
        
        deals = json.loads(self.request.get('deals'))
        for d in deals:
            category_name = d['category']
            identifier = d['dealId']
            deal = Deal(parent=category_key(category_name))    
            deal.category = category_name    
            deal.image = d['imageUrl']
            deal.currentPrice = d['dealPrice']
            deal.title = d['dealTitleTruncated']         
            deal.place = d['cityUrlName']
            deal.orignalPrice = d['dealOldPrice']
            deal.identifier = identifier
            deal.extra = d['dealTitle']
            deal.link ='http://www.groupon.fr' + d['dealPermaLink']
            deal.put()
            
            keywords = d['dealTitle'].split()
            for keyword in keywords:
                if filter_keyword(keyword):
                    if keyword in Deals.index:
                        Deals.index[keyword.lower()].append([identifier, 0])
                    else:
                        Deals.index[keyword.lower()] = [[identifier, 0]]
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Deals stored successfully into local database!')


