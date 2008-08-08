import facebook
import cgi
import wsgiref.handlers

from google.appengine.ext import webapp

class FacebookApp(webapp.RequestHandler):
    def get(self):		
        self.doStuff()
        
    def doStuff(self):		
        api_key = '33205eaaaac54185ceea4f2f92c48152'
        secret_key = '955446cfa27c01e9d67c788337081e99'
        
        facebookapi = facebook.Facebook(api_key, secret_key)
        
        if facebookapi.check_session(self.request):            
            pass
        else:           
           url = facebookapi.get_add_url()
           #self.response.out.write('<fb:redirect url="' + url + '" />')
           #self.response.out.write('<a href="' + url + '">install</a>')
           self.redirect(url)
           return
        
            
        self.response.out.write(facebookapi.session_key + '<br/>')
        self.response.out.write(facebookapi.uid + '<br/>')
        
        info = facebookapi.users.getInfo([facebookapi.uid], ['name'])[0]
        
        self.response.out.write('Your Name: ' + info['name'] + '<br/>')