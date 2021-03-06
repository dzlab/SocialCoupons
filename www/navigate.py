import cgi
import datetime
import urllib
import wsgiref.handlers
import os

from google.appengine.ext.webapp import template
import webapp2
from www.models.deal import *

class Navigator(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        if self.request.get('category'):
            category_name = self.request.get('category')
            deals_query= Deal.all().ancestor(category_key(category_name)).order('-date')
            template_values['deals'] = deals_query.fetch(50)
        else:
            deals = Deal.all().fetch(50)
            categories = []
            for deal in deals:
                if deal.category not in categories:
                    categories.append(deal.category)
            template_values['categories'] = categories
               
        path = os.path.join(os.path.dirname(__file__), 'views/navigate.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        category_name = self.request.get('category')
        category = Deal(parent=category_key(category_name))        
        category.url = self.request.get('url')
        category.tags = self.request.get('tags')
        category.comment = self.request.get('comment')            
        category.put()
        self.redirect('/?' + urllib.urlencode({'saved': True}))
      