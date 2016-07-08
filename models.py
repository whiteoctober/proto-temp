from google.appengine.ext import ndb

class Person(ndb.Model):
    name = ndb.StringProperty()
    gender = ndb.StringProperty()
    age = ndb.IntegerProperty()
