# -*- coding: utf-8 -*-

from handlers import BaseHandler
from feature_models import Feature, FeatureBet, FeaturePerformance
from datetime import timedelta
from user_data.user_models import UserData
from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials
import httplib2
from apiclient.discovery import build

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

        feature_name = self.request.get('feature-name')
        summary = self.request.get('summary')
        KPIs = self.request.get('KPI')
        new_feature = Feature(name=feature_name,
                            summary=summary,
                            KPIs=KPIs.strip().split(','),
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
        features = Feature.query().fetch()
        performances = FeaturePerformance.query().fetch()
        data = {
            'features': features,
            'performances': performances
        }
        return self.render('feature/create-feature-bet.html', data)
        

    def post(self):

        # create or update feature bet
        user = UserData.get_current_user()
        if not user.is_server_admin():  # make sure user has an account to create course
            self.redirect('/')

        feature_key = self.request.get('feature_wanted')
        feature = Feature.get_by_id(int(feature_key))

        performance_key = self.request.get('performance_wanted')
        performance = FeaturePerformance.get_by_id(int(performance_key))

        options = self.request.get('options').split('\n')
        start_time = self.request.get('start_time')
        end_time = self.request.get('end_time')
        billing_time = self.request.get('billing_time')

        new_bet = FeatureBet(performance_bet=performance,
                            bet_options=options,
                            start_time=start_time,
                            end_time=end_time,
                            billing_time=billing_time
                            )

        new_bet.put()

        self.redirect('/')  # 


class UpdateUserFeatureBet(BaseHandler):

    def post(self):

        # update user's bet on certain feature_bet
        # remember to check if user is already bet on this feature_bet
        pass
