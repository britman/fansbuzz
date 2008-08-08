import facebook
import cgi
import wsgiref.handlers
import os

from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp import template

class ContactController(webapp.RequestHandler):
    def get(self):
        template_values = None
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values)) 
        
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        message = self.request.get('message')
        
        mail.send_mail(sender="britman@gmail.com",
                        to = "hello@fansbuzz.com",
                        subject = "A message on FansBuzz from: " + name,
                        body = message + ', email address provided is: ' + email)
        template_values = {
            'confirmation': '<b>Thankyou. Your message has been sent.</b>',   
        }
        path = os.path.join(os.path.dirname(__file__), 'contact.html')
        self.response.out.write(template.render(path, template_values))
        