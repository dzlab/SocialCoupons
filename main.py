import webapp2

from www.search import Search
from www.navigate import Navigator
#from www.index import Index
from www.manage import Manager

app = webapp2.WSGIApplication([
    ('/', Search),
    ('/manage', Manager),
    ('/navigate', Navigator),
    ('/search', Search)
], debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()