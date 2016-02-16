# -*- coding: utf-8 -*-

from handlers import BaseHandler
from feature_models import Feature, FeatureBet, FeaturePerformance
import datetime
from user_data.user_models import UserData
from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials
import httplib2
from apiclient.discovery import build
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
        scheduled_update_date_str = self.request.get('scheduled_update_date')
        scheduled_update_date_arr = scheduled_update_date_str.split('-')
        scheduled_update_date = datetime.datetime(int(scheduled_update_date_arr[0]), int(scheduled_update_date_arr[1]), int(scheduled_update_date_arr[2]))
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



        self.redirect('/')  # 


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

        # get feature bets by feature
        # get user_feature bets by feature bets
        # get feature performance by feature

        # show all these data in the proper way
        data = {
            'feature': feature,
            'feature_KPIs': feature_KPIs,
            'feature_bets': '{{}}',
            'feature_performance': '{{}}'
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
        pass

    def post(self):

        # create or update feature bet
        pass


class UpdateUserFeatureBet(BaseHandler):

    def post(self):

        # update user's bet on certain feature_bet
        # remember to check if user is already bet on this feature_bet
        pass

class ListFeaturePerformance(BaseHandler):

    def get(self):
        logging.info('ShowPerformance')
        user = UserData.get_current_user()
        feature_performances = FeaturePerformance.query().fetch()
        data = {
            'feature_performances': feature_performances
        }
        return self.render('feature/show-performance.html', data)
        pass
