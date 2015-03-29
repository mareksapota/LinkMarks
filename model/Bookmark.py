import urllib.request
import json

from PressUI.cherrypy.Parse import ParseObjFB
from PressUI.cherrypy.Parse import ParseQuery

class Bookmark(ParseObjFB):
    def __init__(self, **kwargs):
        ParseObjFB.__init__(
            self,
            {
                'name': {'type': str},
                'url': {'type': str},
                'keyword': {'type': str, 'nullable': True},
                'suggestions_url': {'type': str, 'nullable': True},
                'tags': {'type': str},
            },
            kwargs,
        )

    def get_suggestions(self, query, user_agent, limit):
        # Don’t forward trivial queries.
        if self.suggestions_url is None or len(query.strip()) == 0:
            return None
        url = self.suggestions_url.replace('%s', query)
        req = urllib.request.Request(
            url,
            headers = { 'User-Agent': user_agent },
        )
        timeout = 15
        ret = urllib.request.urlopen(req, timeout = timeout)
        results = json.loads(ret.read().decode('utf-8'))
        ret.close()
        return results[1][:limit]

    def search(self, query):
        if self.keyword is None:
            raise Exception('This bookmark does not have a keyword')
        return self.url.replace('%s', query)

    @staticmethod
    def __sort_results(bookmarks):
        # Keyword bookmarks should be displayed first.
        keyword = []
        non_keyword = []
        for bookmark in bookmarks:
            if bookmark.keyword is not None:
                keyword.append(bookmark)
            else:
                non_keyword.append(bookmark)
        return keyword + non_keyword

    @staticmethod
    def gen_find_all(query, limit = None):
        name_query = Bookmark.query_safe().matches(
            'name',
            query,
            case_insensitive = True,
        )
        url_query = Bookmark.query_safe().matches('url', query)
        tag_query = Bookmark.query_safe().matches('tags', query)
        query = ParseQuery.or_(name_query, url_query, tag_query)
        def fun(bookmarks):
            return Bookmark.__sort_results(bookmarks)
        return query.ascending('name').limit(limit).gen_find().then(fun)

    @staticmethod
    def gen_find_keyword(keyword):
        p = Bookmark.query_safe().equal_to('keyword', keyword).gen_find()
        def fun(bookmarks):
            if len(bookmarks) == 1:
                return bookmarks[0]
            return None
        return p.then(fun)

    @staticmethod
    def all():
        return Bookmark.__sort_results(
            Bookmark.query_safe().ascending('name').find()
        )
