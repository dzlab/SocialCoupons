
from google.appengine.ext import db


class Deals:
    """Static variable holding index information"""
    index = {} #Index over the stored data of the form {'word':[[deal_identifier, number_of_user_clicks],[]],..} 
    cache = {} #a cache to hold clicked URLs to give them first as a response for subsequent queries

def build_index():
    if len(Deals.index)>0:
        return Deals.index
    deals = Deal.all().fetch(1000)
    for deal in deals:
        keywords = deal.extra.split()
        for keyword in keywords:
            if filter_keyword(keyword):
                if keyword in Deals.index:
                    Deals.index[keyword.lower()].append([deal.identifier, 0])
                else:
                    Deals.index[keyword.lower()] = [[deal.identifier, 0]]
    return Deals.index
    
    
class Deal(db.Model):    
    """Models an individual deal entry with an author, content, and date """
    category = db.StringProperty(multiline=False) # category of the deal
    image = db.StringProperty(multiline=False) # URL to image of the deal
    identifier = db.IntegerProperty() # deal identifier
    title    = db.StringProperty(multiline=True) # title text of the deal
    place = db.StringProperty(multiline=False) # details about corresponding place
    extra = db.StringProperty(multiline=True) # additional information about the deal
    expiration  = db.StringProperty(multiline=False) # text about the deal expiration date dd/mm/yyyy
    orignalPrice = db.StringProperty(multiline=False) # original price of the deal
    currentPrice = db.StringProperty(multiline=False) # deal current price
    link = db.StringProperty(multiline=False) # link to deal web page
    date = db.DateTimeProperty(auto_now_add=True)
    
def category_key(category_name=None):
    """Constructs a datastore key for a Deal entity with category_name"""
    return db.Key.from_path('Deal', category_name or 'default_category')

"""A method for filtering unwanted words"""
def filter_keyword(keyword):
    blacklist = ['ces','sans', 'all', 'eux', 'pas', 'une', 'vos', 'des', 'avec', 'ses', 'ces', ]
    if len(keyword)<3 or keyword.lower() in blacklist:
        return False
    if keyword.isalpha():
        return True
    return False

def get_deals(identifiers):
    if len(identifiers)==0:
        return None
    result = []
    deals = Deal.all().fetch(1000)
    for deal in deals:
        if deal.identifier in identifiers:
            result.append(deal)        
    return result