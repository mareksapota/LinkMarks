import json
import cherrypy

from model.BookmarkBase import BookmarkBase
import model
from utils.session import with_session

class Bookmark(BookmarkBase):
    # Not private so it can be used in BookmarkBase.
    @staticmethod
    def all_query(session):
        return session.query(Bookmark).filter(
            Bookmark.keyword == None,
            Bookmark.fb_user_id == cherrypy.request.fb_user_id,
        )

    @staticmethod
    @with_session()
    def all():
        return BookmarkBase.order(Bookmark.all_query(session)).all()

    def get_url(self):
        return self.url
