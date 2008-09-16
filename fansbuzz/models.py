from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms

class Item(db.Model):
  Author = db.UserProperty()
  Title = db.StringProperty(required=True)
  Description = db.TextProperty()
  Posted_at = db.DateTimeProperty(auto_now_add=True)
  Tags = db.StringListProperty()
  Url = db.LinkProperty()
  ClickCount = db.IntegerProperty()
  
  def created_by(self):
    isemail = self.Author.nickname().find('@')
    if isemail != -1:
        return self.Author.nickname()[:isemail]
    else:
        return self.Author.nickname()
  
  def source(self):
    iscom = self.Url.find('.com')
    iscouk = self.Url.find('.co.uk')
    isnet = self.Url.find('.net')
    if iscom != -1:
        return self.Url[0:iscom+4]
    elif iscouk != -1:
        return self.Url[0:iscouk+6]
    elif isnet != -1:
        return self.Url[0:isnet+4]
    else:
        urlLength = len(self.Url)
        if urlLength < 25:
            return self.Url[0:urlLength]
        else:
            return self.Url[0:25]
            
  def add_click(self):
    if self.ClickCount == None:
      self.ClickCount = 1
    else:
      self.ClickCount = self.ClickCount + 1    
    self.put()
  
  
class ItemForm(djangoforms.ModelForm):
  class Meta:
    model = Item
    exclude = ['Author']

class Comment(db.Model):
  Author = db.UserProperty()
  Comment = db.TextProperty(required=True)
  Posted_at = db.DateTimeProperty(auto_now_add=True)
  Item = db.ReferenceProperty(Item)
  
  def created_by(self):
    isemail = self.Author.nickname().find('@')
    if isemail != -1:
        return self.Author.nickname()[:isemail]
    else:
        return self.Author.nickname()
  
class CommentForm(djangoforms.ModelForm):
  class Meta:
    model = Comment
    exclude = ['Author']