# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
from user_data import user_models
# from report_models import Report


class FeaturePerformance(ndb.Model):

    measured_date = ndb.DateTimeProperty()
    index = ndb.StringProperty()  # should be one of feature KPIs
    value = ndb.FloatProperty()
    scheduled_update = ndb.DateTimeProperty()


class Feature(ndb.Model):

    name = ndb.StringProperty(required=True)
    summary = ndb.TextProperty()
    performances = ndb.KeyProperty(kind=FeaturePerformance, repeated=True)
    # report = ndb.KeyProperty(kind=Report, repeated=True)
    created_time = ndb.DateTimeProperty(auto_now_add=True)
    finish_time = ndb.DateTimeProperty()


class FeatureBet(ndb.Model):

    performance_bet = ndb.KeyProperty(kind=FeaturePerformance)
    bet_options = ndb.StringProperty(repeated=True)
    win_option_index = ndb.IntegerProperty()
    start_time = ndb.DateTimeProperty()
    end_time = ndb.DateTimeProperty()
    billing_time = ndb.DateTimeProperty()


class UserFeatureBet(ndb.Model):
    user = ndb.KeyProperty(kind=user_models.UserData)
    feature_bet = ndb.KeyProperty(kind=FeatureBet)
    option_index_bet = ndb.IntegerProperty()
    bet_capital = ndb.FloatProperty()

