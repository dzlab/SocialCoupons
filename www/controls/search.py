import cgi
import datetime
import urllib
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from www.models.deal import *

class Search(webapp2.RequestHandler):
    """Handle HTTP GET Request by displaying search page"""
    def get(self):
        user = users.get_current_user()
        if user:
            user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {
            'results':[],
        }
        path = os.path.join(os.path.dirname(__file__), '../views/search.html')
        self.response.out.write(template.render(path, template_values))
        
    """Handle HTTP POST Request by displaying search query result"""
    def post(self):
        query = self.request.get('query')
        shopper = users.get_current_user()
        words = query.lower().split()
        keywords = []
        for word in words:
            if filter_keyword(word)==True:
                keywords.append(word)
        updateShopperInfo(shopper, keywords)
        results = []
        tmp = []
        index = build_index()
        """TODO: How could we use a cache?"""
        cache = Deals.cache
        identifiers = []
        """1. Find deals such that its title contains at least one of the words used in the query"""
        for word in keywords:
            if word in index:  
                list_deals = index[word]
                for deal in list_deals:
                    identifiers.append(deal)  
        """2. If there is too much deals satisfying first criteria then this list need to be refined"""
        if len(identifiers) > 10:
            """Refinement is done by selecting only deals that have text containing all words of the query at least once"""
            limit = len(keywords)
            while(limit>0):
                tmp = constrainedSearchResult(index, keywords, identifiers, limit)
                if len(tmp) > 10:
                    break
                """Keep decreasing the bottom limit until having enough refined result or this limit become zero"""
                limit = limit - 1        
            """If limit zero, then no way, just return all previously found deals"""
            if limit == 0:
                tmp = identifiers    
        else:
            """No Refinement is needed as few deals have text containing words from user query"""
            tmp = identifiers      
        """Get the deals corresponding to the found identifiers"""
        results = get_deals(tmp)
        template_values = {
            'deals':results,
            'query':query
        }    
        path = os.path.join(os.path.dirname(__file__), '../views/search.html')
        self.response.out.write(template.render(path, template_values))
        