import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.api import users

from www.models.deal import *

class Navigator(webapp2.RequestHandler):
    """Handle HTTP GET Request by displaying all categories of deals"""
    def get(self):
        user = users.get_current_user()
        if user:
            user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))
        template_values = {}
        if self.request.get('category'):
            category_name = self.request.get('category')
            deals_query = Deal.all().ancestor(category_key(category_name)).order('-date')
            
            template_values['deals'] = deals_query.fetch(1000)
        else:
            deals = Deal.all().fetch(10000)
            categories = []
            for deal in deals:
                if deal.category not in categories:
                    categories.append(deal.category)
            template_values['categories'] = categories
               
        path = os.path.join(os.path.dirname(__file__), '../views/navigate.html')
        self.response.out.write(template.render(path, template_values))
        
    """Handle HTTP POST Request by displaying all deals for a given category stated as parameter in the request"""
    def post(self):
        category_name = self.request.get('category')
        category = Deal(parent=category_key(category_name))        
        category.url = self.request.get('url')
        category.tags = self.request.get('tags')
        category.comment = self.request.get('comment')            
        category.put()
        self.redirect('/?' + urllib.urlencode({'saved': True}))
      