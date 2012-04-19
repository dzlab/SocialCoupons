from google.appengine.ext import webapp
from www.models.deal import *
import logging

import json

class Manager(webapp.RequestHandler):    
    """Handle HTTP GET Request by displaying all stored deals"""
    """This is just to check if deals are correctly stored"""
    def get(self):        
        deals = Deal.all().fetch(999999)
        response = 'Number of stored deals: '+ str(len(deals)) +'\n'
        for deal in deals:
            response = response + deal.category + '- '+ deal.title + '\n'            
        #db.delete(Deal.all().fetch(1000))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(response)
        
    """Handle HTTP POST Request by retrieving the deals, creating a JSON object, """
    """Iterating over the list of deals, and store each deal in the database"""
    def post(self):
        if not self.request.get('deals'):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Deals parameter is missing in received request')
        
        deals = json.loads(self.request.get('deals'))
        for d in deals:
            identifier = d['dealId']
            if identifier in Deals.identfiers:
                logging.info('Deal with ID ' + str(identifier) + ' already stored')
                continue
            else:
                Deals.identfiers.append(identifier)
            category_name = d['category']
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
                    word = keyword.lower()
                    if keyword in Deals.index:
                        Deals.index[word].append(identifier)
                    else:
                        Deals.index[word] = [identifier]
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Deals stored successfully into local database!')


