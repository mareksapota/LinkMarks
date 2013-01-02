from sqlalchemy import Sequence, Column
from sqlalchemy import Integer, String
from sqlalchemy import or_

import urllib
import json

from model.Base import Base
import model

# Convert tags string to internal representation.
def tags_to_intern(tags):
    return ",".join(map(lambda t: t.strip(), tags.split(",")))

# Inverse of the previous method.
def intern_to_tags(tags):
    return tags.replace(",", ", ")

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(
        Integer,
        Sequence("bookmarks_id_seq"),
        primary_key = True
    )

    name = Column(String, nullable = False)
    url = Column(String, nullable = False)
    keyword = Column(String)
    suggestions_url = Column(String)
    # Coma delimited list of tags.
    tags = Column(String, nullable = False)

    @staticmethod
    def find_keyword(keyword):
        session = model.Session()
        query = session.query(Bookmark).filter(Bookmark.keyword == keyword)
        try:
            return query.one()
        except:
            # Multiple or no results.
            return None

    @staticmethod
    def find_all(query, count = None):
        like_query = "%{0}%".format(query)
        session = model.Session()
        query = session.query(Bookmark).filter(or_(
            Bookmark.name.like(like_query),
            Bookmark.url.like(like_query),
            Bookmark.tags.like(like_query)
        )).order_by(
            Bookmark.name
        ).order_by(
            Bookmark.id
        )
        if count is not None:
            query = query.limit(count)
        return query.all()

    @staticmethod
    def new(name, url, keyword, tags, suggestions_url):
        session = model.Session()
        bookmark = Bookmark()
        bookmark.name = ""
        bookmark.url = ""
        bookmark.tags = ""
        session.add(bookmark)
        session.commit()
        id = bookmark.id
        session.close()
        Bookmark.update(id, name, url, keyword, tags, suggestions_url)

    @staticmethod
    def update(id, name, url, keyword, tags, suggestions_url):
        bookmark = Bookmark.get(id)
        session = model.Session()
        bookmark.name = name
        bookmark.url = url.strip()
        if keyword:
            bookmark.keyword = keyword
        else:
            bookmark.keyword = None
        if suggestions_url:
            bookmark.suggestions_url = suggestions_url
        else:
            bookmark.suggestions_url = None
        bookmark.tags = tags_to_intern(tags)
        session.add(bookmark)
        session.commit()

    @staticmethod
    def get(id):
        session = model.Session()
        bookmark = session.query(Bookmark).filter(Bookmark.id == id).one()
        session.close()
        return bookmark

    @staticmethod
    def delete(id):
        bookmark = Bookmark.get(id)
        session = model.Session()
        session.delete(bookmark)
        session.commit()

    def get_tag_string(self):
        return intern_to_tags(self.tags)

    def get_tag_list(self):
        if self.tags:
            return self.tags.split(',')
        else:
            return []

    def get_keyword(self):
        return "" if self.keyword is None else self.keyword

    def get_suggestions_url(self):
        return "" if self.suggestions_url is None else self.suggestions_url

    def search(self, query):
        url = self.url
        if self.keyword is not None:
            query = query[len(self.keyword) + 1:]
            url = url.replace("%s", query)
        return url

    def get_suggestions(self, query, user_agent):
        url = self.suggestions_url
        term = query[len(self.keyword) + 1:]
        results = None
        if (
            # Don't forward trivial queries.
            len(term) > 0 and
            url is not None and
            self.keyword is not None
        ):
            url = url.replace("%s", term.replace(" ", "+"))
            req = urllib.request.Request(
                url,
                headers = { "User-Agent": user_agent }
            )
            req = urllib.request.urlopen(req)
            results = req.read()
            req.close()
            results = json.loads(results.decode("UTF-8"))
            results = [
                query,
                ["{0} {1}".format(self.keyword, s) for s in results[1]]
            ]
        return results
