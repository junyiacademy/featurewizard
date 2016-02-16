from google.appengine.ext import ndb


class Report(ndb.Model):

    name = ndb.StringProperty()
    report_file_id = ndb.StringProperty()
    publish_time = ndb.DateTimeProperty()
