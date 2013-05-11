# -*- coding: utf-8 -*-

import urllib
import urllib.parse
import json
import cherrypy

from model.BookmarkBase import BookmarkBase
import model
from utils.session import with_session

class KeywordBookmark(BookmarkBase):
    # Not private so it can be used in BookmarkBase.
    @staticmethod
    def all_query(session):
        return session.query(KeywordBookmark).filter(
            KeywordBookmark.keyword != None,
            KeywordBookmark.fb_user_id == cherrypy.request.fb_user_id,
        )

    @staticmethod
    @with_session()
    def find(keyword, session = None):
        query = KeywordBookmark.all_query(session) \
                .filter(KeywordBookmark.keyword == keyword)
        try:
            return query.one()
        except:
            # Multiple or no results.
            return None

    @staticmethod
    @with_session()
    def all(session = None):
        return BookmarkBase.order(KeywordBookmark.all_query(session)).all()

    def get_keyword(self):
        return self.keyword

    def search(self, query_body):
        return self.url.replace("%s", query_body)

    def get_url(self):
        # Replace the search param with an empty string, like search("") but
        # works for both KeywordBookmark and Bookmark
        return self.url.replace("%s", "")

    def get_suggestions(self, query, user_agent):
        if query.keyword() != self.keyword:
            return None
        term = query.body()
        # Don’t forward trivial queries.
        if self.suggestions_url is None or len(term) == 0:
            return None
        url = self.suggestions_url.replace("%s", term)
        req = urllib.request.Request(
            url,
            headers = { "User-Agent": user_agent }
        )
        req = urllib.request.urlopen(req)
        results = req.read()
        req.close()
        results = json.loads(results.decode("UTF-8"))
        return [
            str(query.url_unsafe()),
            ["{0} {1}".format(self.keyword, s) for s in results[1]],
        ]
