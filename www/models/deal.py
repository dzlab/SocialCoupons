
from google.appengine.ext import db


class Deals:
    """Static variable holding index information"""
    index = {} #Index over the stored data of the form {'word':[[deal_identifier, number_of_user_clicks],[]],..} 
    cache = {} #a cache to hold clicked URLs to give them first as a response for subsequent queries
    identfiers = [] #list of all identifiers stored in the database

"""A method to build the search index and stored in memory for accelerating search algorithm"""
def build_index():
    if len(Deals.index)>0:
        return Deals.index
    deals = Deal.all().fetch(10000)
    for deal in deals:
        keywords = deal.extra.split()
        for keyword in keywords:
            if filter_keyword(keyword):
                word = keyword.lower()
                if keyword in Deals.index:
                    Deals.index[word].append(deal.identifier)
                else:
                    Deals.index[word] = [deal.identifier]
    return Deals.index
    
"""A method used to refine search by returning identifiers of deals that are indexed by at least 'limit' word"""
def constrainedSearchResult(index, keywords, identifiers, limit):
    result = []
    for id in identifiers:
        occurrence = 0
        for word in keywords:
            if word in index:
                if id in index[word]:
                    occurrence = occurrence + 1
        """Add this deal to query result if it is indexed by at least by 'limit' word from words of the user query"""
        if occurrence >= limit:
            result.append(id)
    return result

"""A class gathering information about users"""
"""The queries attribute hold all words used by the corresponding used in his last queries"""
class Shopper(db.Model):
    username = db.UserProperty()
    queries = db.StringProperty(multiline=False)
    #queries = db.StringListProperty()

"""A method to get queries history for a given shopper"""
def getShopperQuery(user):
    shoppers = Shopper.all().fetch(1000)
    for shopper in shoppers:
        if shopper.username == user:
            return shopper.queries
    return None

"""Update user profile (historical queries) with new information (new submitted query)"""
def updateShopperInfo(user, keywords):
    found = False
    shoppers = Shopper.all().fetch(1000)
    for shopper in shoppers:
        if shopper.username == user:
            found = True
            queries = shopper.queries
            for keyword in keywords:
                if filter_keyword(keyword)==True and queries.find(keyword)==-1:
                    queries = queries + ' ' + keyword
            shopper.queries = queries
            shopper.put()
    if not found:
        shopper = Shopper()
        shopper.username = user
        queries = ''
        for keyword in keywords:
            if filter_keyword(keyword)==True and queries.find(keyword)==-1:
                queries = queries + ' ' + keyword
        shopper.queries = queries
        shopper.put()

"""A subclass of db.Model representing how a deal is stored by GAE"""    
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


"""A method to get a key for a category of deals, 
to store deals in such way they will be gathered by their respective category"""    
def category_key(category_name=None):
    """Constructs a datastore key for a Deal entity with category_name"""
    return db.Key.from_path('Deal', category_name or 'default_category')


"""A method for filtering unwanted words, return False if word is unwanted, True otherwise"""
def filter_keyword(keyword):
    blacklist = ['ces','sans', 'all', 'eux', 'pas', 'une', 'vos', 'des', 'avec', 'ses', 'ces']
    if len(keyword)<3 or keyword.lower() in blacklist:
        return False
    if keyword.isalpha():
        return True
    return True

"""Remove unwanted characters from a word"""

""" A method to find deals for a given list of deal identifiers """
def get_deals(identifiers):
    if len(identifiers)==0:
        return None
    result = []
    deals = Deal.all().fetch(10000)
    for deal in deals:
        if deal.identifier in identifiers:
            result.append(deal)        
    return result