import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Item(db.Model):
  author = db.UserProperty()
  title = db.StringProperty(multiline=True)
  description = db.TextProperty()
  posted_at = db.DateTimeProperty(auto_now_add=True)

class MainHandler(webapp.RequestHandler):

  def get(self):
    items_query = Item.all().order('-posted_at')
    items = items_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'items': items,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))
    
  def post(self):
    checkAuth()
    item = Item()    
    item.author = users.get_current_user()      
    item.title = self.request.get('title')
    item.description = self.request.get('description')
    

def main():
  application = webapp.WSGIApplication([('.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
