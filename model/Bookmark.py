import cherrypy
import urllib.request
import json

from model.Parse import ParseObj, ParseQuery

class Bookmark(ParseObj):
    def __init__(self, **kwargs):
        if "fb_user_id" not in kwargs:
            kwargs["fb_user_id"] = cherrypy.request.fb_user_id

        ParseObj.__init__(
            self,
            {
                "fb_user_id": {"type": int},
                "name": {"type": str},
                "url": {"type": str},
                "keyword": {"type": str, "nullable": True},
                "suggestions_url": {"type": str, "nullable": True},
                "tags": {"type": str},
            },
            kwargs,
        )

    def str_tags(self):
        tags = self.tags.split(",")
        return ", ".join([t.strip() for t in tags])

    def has_tags(self):
        return self.tags.strip() != ""

    def str_keyword(self):
        return self.keyword if self.keyword else ""

    def str_suggestions_url(self):
        return self.suggestions_url if self.suggestions_url else ""

    def str_url(self):
        # Replace the search param with an empty string
        if self.keyword is not None:
            return self.url.replace("%s", "")
        return self.url

    def search(self, query_body):
        if self.keyword is None:
            raise Exception("This bookmark does not have a keyword")
        return self.url.replace("%s", query_body)

    def get_suggestions(self, query, user_agent, limit):
        if query.keyword() != self.keyword:
             return None
        term = query.body()
        # Don’t forward trivial queries.
        if self.suggestions_url is None or len(term) == 0:
            return None
        url = self.suggestions_url.replace("%s", term)
        req = urllib.request.Request(
            url,
            headers = { "User-Agent": user_agent },
        )
        ret = urllib.request.urlopen(req)
        results = ret.read()
        ret.close()
        results = json.loads(results.decode("UTF-8"))[1][:limit]
        return [
            str(query.url_unsafe()),
            ["{0} {1}".format(self.keyword, s) for s in results],
        ]

    @staticmethod
    def get_safe(objectId):
        bookmark = Bookmark.get(objectId)
        if bookmark.fb_user_id != cherrypy.request.fb_user_id:
            raise Exception("Unauthorised access")
        return bookmark

    @staticmethod
    def query_safe():
        return Bookmark.query().equal_to(
            "fb_user_id",
            cherrypy.request.fb_user_id,
        )

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
        query = str(query.url_unsafe())
        name_query = Bookmark.query_safe().matches("name", query)
        url_query = Bookmark.query_safe().matches("url", query)
        tag_query = Bookmark.query_safe().matches("tags", query)
        query = ParseQuery.or_(name_query, url_query, tag_query)
        def fun(bookmarks):
            return Bookmark.__sort_results(bookmarks)
        return query.ascending("name").limit(limit).gen_find().then(fun)

    @staticmethod
    def gen_find_keyword(keyword):
        p = Bookmark.query_safe().equal_to("keyword", keyword).gen_find()
        def fun(bookmarks):
            if len(bookmarks) == 1:
                return bookmarks[0]
            return None
        return p.then(fun)

    @staticmethod
    def all():
        return Bookmark.__sort_results(
            Bookmark.query_safe().ascending("name").find()
        )
