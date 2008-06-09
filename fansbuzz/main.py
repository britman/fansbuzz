import cgi
import wsgiref.handlers
import os
import models
import logging

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainController(webapp.RequestHandler):
  def get(self):
    tag = self.request.get('tag')
    logging.debug('tag=' + tag)
    items_to_display = 10
    if tag == "":
        items_query = models.Item.all().order('-Posted_at')
    else:
        items_query = db.GqlQuery("SELECT * FROM Item WHERE Tags = :1", tag)
    items_count = items_query.count()
    items = items_query.fetch(items_to_display)
        
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
    
class ItemController(webapp.RequestHandler):
  def get(self):
    logging.debug('entering item form')
    if users.get_current_user():
        template_values = {
          'form': models.ItemForm(),
          }
          
        path = os.path.join(os.path.dirname(__file__), 'NewItem.html')
        self.response.out.write(template.render(path, template_values))   
    
    else:
        redir = users.create_login_url(self.request.uri)
        self.redirect(redir)
        
  def post(self):
    if users.get_current_user():
        data = models.ItemForm(data=self.request.POST)  
        logging.debug(self.request.POST)        
        if data.is_valid():                 
            item = data.save(commit=False)    
            item.Author = users.get_current_user()
            tags = self.request.get('Tags',allow_multiple=True)
            logging.debug(tags)    
            item.Tags = []
            for t in tags:
                item.Tags.append(t)
            item.put()
            self.redirect('/')        
        else:
            template_values = {
            'form': data,    
            }
            path = os.path.join(os.path.dirname(__file__), 'NewItem.html')
            self.response.out.write(template.render(path, template_values))   
    else:
        redir = users.create_login_url("/")
        self.redirect(redir)

class CommentController(webapp.RequestHandler):
  def get(self): 
    item = models.Item.get(self.request.get('k'))
    template_values = {
        'form' : models.CommentForm(),
        'item' : item,
        'loggedin' : users.get_current_user(),
        'url' : users.create_login_url(self.request.uri)
    }
    path = os.path.join(os.path.dirname(__file__), 'Comment.html')
    self.response.out.write(template.render(path, template_values)) 

        
  def post(self):
    if users.get_current_user():
        data = models.CommentForm(data=self.request.POST)
        item = models.Item.get(self.request.get('k'))
        if data.is_valid():
            comment = data.save(commit=False)
            comment.Author = users.get_current_user()            
            comment.Item = item
            comment.put()
            self.redirect('/') 
        else:
            template_values = {
                'form' : data,
                'item' : item,
                'loggedin' : users.get_current_user(),
                'url' : users.create_login_url(self.request.uri)
            }
            path = os.path.join(os.path.dirname(__file__), 'Comment.html')
            self.response.out.write(template.render(path, template_values)) 
    else:
        redir = users.create_login_url("/")
        self.redirect(redir)
    
   

def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainController),('/item', ItemController),('/comment', CommentController)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
