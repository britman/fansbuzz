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
  
class ItemForm(djangoforms.ModelForm):
  class Meta:
    model = Item
    exclude = ['Author']

class Comment(db.Model):
  Author = db.UserProperty()
  Comment = db.StringProperty(required=True)
  Posted_at = db.DateTimeProperty(auto_now_add=True)
  Item = db.ReferenceProperty(Item)
  
class CommentForm(djangoforms.ModelForm):
  class Meta:
    model = Comment
    exclude = ['Author']