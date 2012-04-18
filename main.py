import webapp2

from www.controls.search import Search
from www.controls.navigate import Navigator
from www.controls.advice import Advice
from www.controls.manage import Manager

app = webapp2.WSGIApplication([
    ('/', Search),
    ('/manage', Manager),
    ('/navigate', Navigator),
    ('/search', Search),
    ('/advice', Advice)
], debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()