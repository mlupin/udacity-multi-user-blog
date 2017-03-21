from handlers.blog import BlogHandler
from google.appengine.ext import db
from helpers import *
from models.comment import Comment
import time


class AddComment(BlogHandler):
    def get(self, post_id, user_id):
        # Only signed in users can post comments
        # Logged out users are redirected to the login page
        if self.user:
            return self.render('addcomment.html')
        elif not self.user:
            return self.redirect('/signin')

    def post(self, post_id, user_id):
        if self.user:
            content = self.request.get('content')

            if content:
                author = self.user.name
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                comment = Comment(parent=key, user_id=int(user_id),
                                  post_id=int(post_id), content=content,
                                  author=author)
                comment.put()
                time.sleep(0.1)
                # Users are redirected to blog home page after page updates
                return self.redirect('/blog')
            else:
                error = "content, please!"
                return self.render("addcomment.html",
                                   content=content, error=error)
        elif not self.user:
            return self.redirect('/signin')
