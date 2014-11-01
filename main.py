import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from models import *

jinjaEnv = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
    extensions = ['jinja2.ext.autoescape'])


class IndexPage(webapp2.RequestHandler):
    def get(self):
        template = jinjaEnv.get_template('index.html')
        self.response.write(template.render())

class NonAncestorQueryDemoPage(webapp2.RequestHandler):
    def get(self):
        values = { 'heading': 'Non Ancestor Query Demo' }
        
        values['messages'] = Message.query().order(-Message.timestamp)

        template = jinjaEnv.get_template('messages.html')
        self.response.write(template.render(values))

    def post(self):
        m = Message(text = self.request.get('message'))
        m.put()

        self.redirect("/naq")

class AncestorQueryDemoPage(webapp2.RequestHandler):
    def get(self):
        values = { 'heading': 'Ancestor Query Demo' }

        values['messages'] = Message.query(ancestor=ndb.Key('Message', 'all')).order(-Message.timestamp)

        template = jinjaEnv.get_template('messages.html')
        self.response.write(template.render(values))

    def post(self):
        m = Message(text = self.request.get('message'), parent=ndb.Key('Message', 'all'))
        m.put()

        self.redirect("/aq")

application = webapp2.WSGIApplication([
    ('/', IndexPage),
    ('/naq', NonAncestorQueryDemoPage),
    ('/aq', AncestorQueryDemoPage),
], debug=True)
