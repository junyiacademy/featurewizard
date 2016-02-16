# -*- coding: utf-8 -*-

from handlers import BaseHandler
from feature_models import Feature, FeatureBet, FeaturePerformance, UserFeatureBet
import datetime
from user_data.user_models import UserData
from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials
import httplib2
from apiclient.discovery import build
import json
import logging

# credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/drive')
# http = credentials.authorize(httplib2.Http(memcache))
# service = build('drive', 'v2', http=http)


class CreateFeature(BaseHandler):

    def get(self):
        return self.render('feature/create-feature.html')

    def post(self):

        # upload new material on google drive
        user = UserData.get_current_user()
        if not user.is_server_admin():  # make sure user has an account to create course
            self.redirect('/')

        # [TODO]Benny: scheduled_update_date超醜，要改掉
        # [TODO]Benny: new_feature_performance要搬到CreateFeaturePerformance 這個handler
        scheduled_update_date = self.request.get('scheduled_update_date')
        scheduled_update_date = datetime.datetime.strptime(scheduled_update_date, "%Y-%m-%d")
        logging.info('scheduled_update_date: %s' %scheduled_update_date)
        index = self.request.get('performance_index')
        new_feature_performance = FeaturePerformance(
            scheduled_update_date=scheduled_update_date,
            index=index)
        new_feature_performance.put()

        feature_name = self.request.get('feature-name')
        summary = self.request.get('summary')
        KPIs = self.request.get('KPI')
        new_feature = Feature(name=feature_name,
                            summary=summary,
                            KPIs=KPIs.strip().split(','),
                            performances=[new_feature_performance.key]
                            )
        new_feature.put()



        self.redirect('/show-feature/%s' % new_feature.key.id()) # 


class ListFeatures(BaseHandler):

    def get(self):

        features = Feature.query().fetch()
        features.sort(key=lambda x: x.created_time, reverse=True)

        # get related feature_bets
        # create feature bets json
        feature_KPIs = [','.join(f.KPIs) for f in features]

        data = {
            'features': features,
            'feature_KPIs': feature_KPIs
        }

        return self.render('feature/list-features.html', data)


class ShowFeature(BaseHandler):

    def get(self, feature_id):

        user = UserData.get_current_user()
        feature = Feature.get_by_id(int(feature_id))
        feature_KPIs = ','.join(feature.KPIs)
        feature_performance = feature.performances[0].get()
        feature_bets = FeatureBet.get_by_feature_performance(feature_performance)

        # get feature bets by feature
        # get user_feature bets by feature bets
        # get feature performance by feature

        # show all these data in the proper way
        data = {
            'feature': feature,
            'feature_KPIs': feature_KPIs,
            'feature_bets': feature_bets,
            'feature_performance': feature_performance
        }

        return self.render('feature/show-feature.html', data)


class CreateFeaturePerformance(BaseHandler):

    def get(self):

        # get all features to be chose
        # form page to create/update feature performance
        pass

    def post(self):

        # create or update feature performance
        # after update feature performance, check if some feature bet is billing
        pass


class CreateFeatureBet(BaseHandler):

    def get(self):

        # get all features and feature_performance to be chose
        # form page to create/update feature bet
        features = Feature.query().fetch()
        performances = FeaturePerformance.query().fetch()
        data = {
            'features': features,
        }
        return self.render('feature/create-feature-bet.html', data)
        

    def post(self):

        # create or update feature bet
        user = UserData.get_current_user()
        if not user.is_server_admin():  # make sure user has an account to create course
            self.redirect('/')

        feature_key = self.request.get('feature_wanted')
        feature = Feature.get_by_id(int(feature_key))

        options = self.request.get('options').split('\n')
        start_time = self.request.get('start-time')
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        end_time = self.request.get('end-time')
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")

        billing_time = self.request.get('billing-time')
        billing_time = datetime.datetime.strptime(billing_time, "%Y-%m-%d")

        new_bet = FeatureBet(performance_bet=feature.performances[0],
                            bet_options=options,
                            start_time=start_time,
                            end_time=end_time,
                            billing_time=billing_time
                            )

        new_bet.put()

        self.redirect('/show-feature/%s' % feature.key.id()) # 
# 


class UpdateUserFeatureBet(BaseHandler):

    def post(self):

        user = UserData.get_current_user()
        feature_bet_id = self.request.get('feature-bet-id')
        bet_option_index = self.request.get('bet-option')
        bet_capital = self.request.get('bet-capital')

        feature_bet = FeatureBet.get_by_id(int(feature_bet_id))

        user_bet = UserFeatureBet(user=user.key,
                                 feature_bet=feature_bet.key,
                                 option_index_bet=int(bet_option_index),
                                 bet_capital=float(bet_capital))
        user_bet.put()


class ListFeaturePerformance(BaseHandler):

    def get(self):
        logging.info('ShowPerformance')
        user = UserData.get_current_user()
        features = Feature.query().fetch()
        feature_performances = []
        for feature in features:
            performance = feature.performances[0].get()
            feature_performances.append({
                'name': feature.name,
                'index': performance.index,
                'scheduled_update_date': performance.scheduled_update_date,
                'key': performance.key.id()
            })
        logging.info('feature_performances: %s' %feature_performances)
        data = {
            'feature_performances': feature_performances
        }
        return self.render('feature/show-performance.html', data)

class ModifyFeaturePerformance(BaseHandler):

    def post(self):
        data = json.loads(self.request.body)
        index = data['index']
        scheduled_update_date = data['scheduled_update_date']
        scheduled_update_date = datetime.datetime.strptime(scheduled_update_date, "%Y-%m-%d")
        key_id = data['key_id']
        feature_performance = FeaturePerformance.get_by_id(int(key_id))
        if index:
            feature_performance.index = index
        if scheduled_update_date:
            feature_performance.scheduled_update_date = scheduled_update_date
        feature_performance.put()
        return

class FinishFeaturePerformance(BaseHandler):

    def post(self):
        data = json.loads(self.request.body)
        value = data['value']
        key_id = data['key_id']
        feature_performance = FeaturePerformance.get_by_id(int(key_id))
        feature_performance.measured_date = datetime.datetime.now()
        feature_performance.value = float(value)
        feature_performance.put()
        return
