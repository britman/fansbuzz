import cgi
import wsgiref.handlers
import os
import models
import logging
import time, datetime

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from datetime import datetime

class MainController(webapp.RequestHandler):
  def get(self):
    tag = self.request.get('tag')
    mode = self.request.get('mode')
    type = self.request.get('type')
    
    try:
        start = int(self.request.get('start'))
    except ValueError:
        start = 0
        
    logging.debug('tag=' + tag)
    items_to_display = 10
    if tag == "":
        if type == "buzz":
            items_query = db.GqlQuery("SELECT * FROM Item ORDER BY ClickCount DESC")
            page_url = "?start="
            back_page_url = page_url
            rss_url = "?mode=RSS"
            tag_label = ""
        else:
            items_query = db.GqlQuery("SELECT * FROM Item ORDER BY Posted_at DESC")
            page_url = "?start="
            back_page_url = page_url
            rss_url = "?mode=RSS"
            tag_label = ""
    else:
        items_query = db.GqlQuery("SELECT * FROM Item WHERE Tags = :1 ORDER BY Posted_at DESC", tag)
        page_url = "?tag=" + tag + "&start="
        back_page_url = page_url
        rss_url = "?tag=" + tag + "&mode=RSS"
        tag_label = " : " + tag
        
    items_count = items_query.count()
    items = items_query.fetch(items_to_display,start)
    
    nextPageStart = items_to_display + start
    previousPageStart = start - items_to_display
    
    logging.debug(str(items_count) + "," + str(items_to_display) + "," + str(nextPageStart) + ",")
    if items_count > items_to_display and items_count > nextPageStart:
        page_url =  page_url + str(nextPageStart)
    else:
        page_url = ""
    
    #previous link setup
    if start == 0:    
        back_page_url = ""
    else:
        back_page_url = back_page_url + str(previousPageStart)
        
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Already got a google account...login here!'

    template_values = {
      'items': items,
      'page_url': page_url,
      'back_page_url': back_page_url,
      'url': url,
      'url_linktext': url_linktext,
      'rss_url': rss_url,
      'tag': tag_label,      
      }

    if mode == "RSS":
        template_values = {
          'items': items,
          'url': self.request.uri,
          'build_date': datetime.now(),
          'tag': tag,
        }
        path = os.path.join(os.path.dirname(__file__), 'rss.xml')
        self.response.out.write(template.render(path, template_values)) 
    else:
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values)) 
    
class ItemController(webapp.RequestHandler):
  def get(self):
    logging.debug('entering item form')
    clubtags = ["Arsenal","Aston Villa","Barnsley","Blackburn","Blackpool","Bolton","Bristol City","Burnley","Cardiff","Charlton","Chelsea","Colchester","Coventry","Crystal Palace","Everton","Hull","Ipswich","Leicester","Liverpool","Man City ","Man Utd","Middlesbrough ","Newcastle","Norwich","Plymouth","Portsmouth","Preston","QPR","Scunthorpe","Sheff Utd","Sheff Wed","Southampton","Stoke","Sunderland","Tottenham","Watford","West Brom","West Ham","Wigan","Wolverhampton","Swansea","Nottm Forest","Doncaster","Carlisle","Leeds","Southend","Brighton","Oldham","Northampton","Huddersfield","Tranmere","Walsall","Swindon","Leyton Orient","Hartlepool","Bristol Rovers","Millwall","Yeovil","Cheltenham","Crewe","Bournemouth","Gillingham","Port Vale","Luton","Milton Keynes Dons","Peterborough","Hereford","Stockport","Rochdale","Darlington","Wycombe","Chesterfield","Rotherham","Bradford","Morecambe","Barnet","Bury","Brentford","Lincoln City","Grimsby","Accrington Stanley","Shrewsbury","Macclesfield","Dag & Red","Notts County","Chester","Mansfield","Wrexham"]
    clubtags.sort()
    if users.get_current_user():
        template_values = {
          'form': models.ItemForm(),
          'tags': clubtags
          }
          
        path = os.path.join(os.path.dirname(__file__), 'NewItem.html')
        self.response.out.write(template.render(path, template_values))   
    
    else:
        redir = users.create_login_url(self.request.uri)
        self.redirect(redir)
        
  def post(self):
    if self.request.get('Auth') == "britman@gmail.com":
        user = users.User("britman@gmail.com")   
    else: 
        user = None
    
    if user != None or users.get_current_user():
        data = models.ItemForm(data=self.request.POST)  
        logging.debug(self.request.POST)        
        if data.is_valid():                 
            item = data.save(commit=False)    
            if user != None:
                item.Author = user
            else:
                item.Author = users.get_current_user()
            
            if self.request.get('Pub') != "":
            #"Tue, 10 Jun 2008 22:19:16 GMT"
                timestring = self.request.get('Pub')
                time_format = "%a, %d %b %Y %H:%M:%S GMT"
                item.Posted_at = datetime.fromtimestamp(time.mktime(time.strptime(timestring, time_format)))

            tags = self.request.get('Tags',allow_multiple=True)
            logging.debug(tags)    
            item.Tags = []
            count = 0;
            for t in tags:
                if count < 10:
                    item.Tags.append(t)
                    count = count+1
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
            self.redirect(self.request.uri) 
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
    
class ClickController(webapp.RequestHandler):
  def get(self): 
      self.redirect("/")
      
  def post(self):        
      item = models.Item.get(self.request.get('id'))
      item.add_click()
    
def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainController),('/item', ItemController),('/comment', CommentController),('/Tag/.*', MainController),('/click', ClickController)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
