# -*- coding: utf-8 -*-

from handlers import BaseHandler
from user_data.user_models import UserData
from comment.comment_models import Comment


class CommentUpdate(BaseHandler):

    def post(self):

        user_id = int(self.request.get('user_id'))
        user = UserData.get_by_id(user_id)
        user = user or UserData.get_current_user()
        if user is None:
            return

        comment_parent_key = self.request.get('comment_parent_key')
        parent =  "# get by key"
        comment_content = self.request.get('content')

        new_comment = Comment(parent=parent.key,
                              comment_user=user.key,
                              comment_content=content
                             )
        new_comment.put()
        return