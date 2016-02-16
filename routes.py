# -*- coding: utf-8 -*-
import sys
import webapp2

import homepage
import login
from features import feature_handler
from comment import comment_handler
import profile


config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '1aqz@SWX3dec$FRV5gtb^HYN7jum*KI<9lo.):P?',
}

reload(sys)
sys.setdefaultencoding('utf-8')
app = webapp2.WSGIApplication([
                              # Admin

                              # Home Page
                              (r'/', feature_handler.ListFeatures),

                              # Admin Page
                              (r'/admin/create-feature', feature_handler.CreateFeature),
                              (r'/admin/create-feature-bet', feature_handler.CreateFeatureBet),

                              (r'/show-feature/(\d+)', feature_handler.ShowFeature),
                              (r'/list-features', feature_handler.ListFeatures),
                              (r'/profile', profile.Profile),
                              (r'/comment-update', comment_handler.CommentUpdate),
                              # Login Page
                              (r'/login-page', login.LoginPage),
                              (r'/logout', login.Logout),
                              (r'/login', login.Login),

                              # Error Pages
                              (r'/*', homepage.NotFoundPage),
                              ], debug=True, config=config)
