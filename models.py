from google.appengine.ext import ndb

class Message(ndb.Model):
    text = ndb.StringProperty(indexed=False)
    timestamp = ndb.DateTimeProperty(auto_now_add=True)
