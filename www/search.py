import cgi
import datetime
import urllib
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
import webapp2

from models.deal import *

class Search(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'results':[],
        }
        path = os.path.join(os.path.dirname(__file__), 'views/search.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        query = self.request.get('query')
        keywords = query.lower().split()
        results = []
        index = build_index()
        cache = Deals.cache
        identifiers = []
        for word in keywords:
            if word in index:  
                list_deals = index[word]
                for deal in list_deals:
                    identifiers.append(deal[0])
        results = get_deals(identifiers)            
        
        template_values = {
            'deals':results,
            'query':query
        }    
        path = os.path.join(os.path.dirname(__file__), 'views/search.html')
        self.response.out.write(template.render(path, template_values))
        