import cgi
import wsgiref.handlers
import os
import models
import logging
import time, datetime
import operator
import facebookapp
import contactcontroller

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users
from datetime import datetime
from datetime import timedelta

class MainController(webapp.RequestHandler):
  def get(self):
    tag = self.request.get('tag')
    mode = self.request.get('mode')
    type = self.request.get('type')
    
    path = self.request.path_info.replace('%20',' ')
    if (path.find('/tag/') == 0):
	  tag = path[5:]

    try:
        start = int(self.request.get('start'))
    except ValueError:
        start = 0
        
    logging.debug('tag=' + tag)
    
    #nav selector classes
    buzzNavClass = ''
    newNavClass = ''
    
    items_to_display = 10
    if tag == "":
        if type == "buzz":            
            #get all the items in the last 24 hours
            compDate=datetime.now() 
            t = timedelta(days=1)
            items_keys_query = db.GqlQuery('SELECT * FROM Item  WHERE Posted_at > :1 ORDER BY Posted_at DESC',compDate-t)   
            items_keys_count = items_keys_query.count()         
            itemkeys = items_keys_query.fetch(items_keys_count,0)
            
            #filter through them to pull out those that have a click count > 0
            buzzitems = [str(elem.key()) for elem in itemkeys if elem.ClickCount > 0]  
            #number of items that will be available to paging
            items_count = len(buzzitems)
            
            #feed the id's back into a GQL query to pull out the list
            if buzzitems:
                items = models.Item.get(buzzitems)
                items.sort(key=operator.attrgetter('ClickCount'),reverse=True)
            else:
                items = None
            
            headline = 'Latest buzz in the last 24 hours'
            buzzNavClass = 'navSel'
        else:
            items_query = db.GqlQuery('SELECT * FROM Item ORDER BY Posted_at DESC')    
            headline = 'Hot off the press - the latest stories as they happen'     
            newNavClass = 'navSel'
 
        tag_label = ""
    else:
        items_query = db.GqlQuery('SELECT * FROM Item WHERE Tags = :1 ORDER BY Posted_at DESC', tag)
        headline = 'All the news for ' + tag  
        tag_label = " : " + tag        

    if type == "buzz":      
        if items:
            items = items[start:start + 10]
        rss_url = "?type=buzz&mode=RSS" 
        page_url = "?type=buzz&start=" 
    else:
        items = items_query.fetch(items_to_display,start)
        items_count = items_query.count()
        rss_url = "?mode=RSS"  
        page_url = "?start=" 

    back_page_url = page_url

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
      'headline': headline,
      'newNavClass': newNavClass,
      'buzzNavClass': buzzNavClass,
      }

    if mode == "RSS":
        template_values = {
          'items': items,
          'url': self.request.uri,
          'build_date': datetime.now(),
          'tag': tag,
          'headline': headline,
        }
        path = os.path.join(os.path.dirname(__file__), 'rss.xml')
        self.response.out.write(template.render(path, template_values)) 
    else:
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values)) 


class ItemController(webapp.RequestHandler):
  def get(self):
    logging.debug('entering item form')
    clubtags = ["Arsenal","Aston Villa","Barnsley","Blackburn","Blackpool","Bolton","Bristol City","Burnley","Cardiff","Charlton","Chelsea","Colchester","Coventry","Crystal Palace","Everton","Hull","Ipswich","Leicester","Liverpool","Manchester City","Man Utd","Middlesbrough ","Newcastle","Norwich","Plymouth","Portsmouth","Preston","QPR","Scunthorpe","Sheffield Utd","Sheff Wed","Southampton","Stoke","Sunderland","Tottenham","Watford","West Brom","West Ham","Wigan","Wolverhampton","Swansea","Nottm Forest","Doncaster","Carlisle","Leeds","Southend","Brighton","Oldham","Northampton","Huddersfield","Tranmere","Walsall","Swindon","Leyton Orient","Hartlepool","Bristol Rovers","Millwall","Yeovil","Cheltenham","Crewe","Bournemouth","Gillingham","Port Vale","Luton","Milton Keynes Dons","Peterborough","Hereford","Stockport","Rochdale","Darlington","Wycombe","Chesterfield","Rotherham","Bradford","Morecambe","Barnet","Bury","Brentford","Lincoln City","Grimsby","Accrington Stanley","Shrewsbury","Macclesfield","Dag & Red","Notts County","Chester","Mansfield","Wrexham"]
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

class SitemapController(webapp.RequestHandler):
  def get(self):
        template_values = {
          'build_date': datetime.now(),
        }
        path = os.path.join(os.path.dirname(__file__), 'Sitemap.xml')
        self.response.out.write(template.render(path, template_values)) 
    
def main():
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainController),('/item', ItemController),('/comment', CommentController),('/tag/.*', MainController),('/click', ClickController),('/fb', facebookapp.FacebookApp),('/contact',contactcontroller.ContactController),('/sitemap',SitemapController)],debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
