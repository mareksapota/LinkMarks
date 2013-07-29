from sqlalchemy import Sequence, Column
from sqlalchemy import Integer, String
from sqlalchemy import or_
import cherrypy

from model.Base import Base
import model
from utils.session import with_session

# Convert tags string to internal representation.
def tags_to_intern(tags):
    return ",".join(map(lambda t: t.strip(), tags.split(",")))

# Inverse of the previous method.
def intern_to_tags(tags):
    return tags.replace(",", ", ")

class BookmarkBase(Base):
    __tablename__ = "bookmarks"

    id = Column(
        Integer,
        Sequence("bookmarks_id_seq"),
        primary_key = True
    )

    fb_user_id = Column(Integer, nullable = False)
    name = Column(String, nullable = False)
    url = Column(String, nullable = False)
    keyword = Column(String)
    suggestions_url = Column(String)
    # Coma delimited list of tags.
    tags = Column(String, nullable = False)

    def get_tag_string(self):
        return intern_to_tags(self.tags)

    def get_keyword(self):
        return self.keyword if self.keyword else ""

    def get_suggestions_url(self):
        return self.suggestions_url if self.suggestions_url else ""

    # Not private so it can be accessed in subclasses
    @staticmethod
    def order(query):
        return query.order_by(BookmarkBase.name).order_by(BookmarkBase.id)

    @staticmethod
    @with_session()
    def find_all(query, count = None, session = None):
        # Deferred import to avoid circular dependencies.
        from model.Bookmark import Bookmark
        from model.KeywordBookmark import KeywordBookmark

        like_query = "%{0}%".format(
            query if query.__class__ == str else query.url_unsafe()
        )
        def add_filter(query):
            query = query.filter(or_(
                BookmarkBase.name.like(like_query),
                BookmarkBase.url.like(like_query),
                BookmarkBase.tags.like(like_query),
            ))
            query = BookmarkBase.order(query)
            if count is not None:
                query = query.limit(count)
            return query
        keyword_bookmarks = add_filter(KeywordBookmark.all_query(session)).all()
        bookmarks = add_filter(Bookmark.all_query(session)).all()

        all_bookmarks = keyword_bookmarks + bookmarks
        if count is not None:
            return all_bookmarks[:count]
        else:
            return all_bookmarks

    @staticmethod
    def all():
        return BookmarkBase.find_all("")

    @staticmethod
    @with_session()
    def get(id, session = None):
        # Deferred import to avoid circular dependencies.
        from model.Bookmark import Bookmark
        from model.KeywordBookmark import KeywordBookmark

        def find(query):
            return query.filter(Bookmark.id == id).one()

        try:
            return find(KeywordBookmark.all_query(session))
        except:
            # Maybe it is a Bookmark?
            pass
        return find(Bookmark.all_query(session))

    @staticmethod
    @with_session(commit = True)
    def delete(id, session = None):
        bookmark = BookmarkBase.get(id)
        session.delete(bookmark)

    @staticmethod
    @with_session(commit = True)
    def new(name, url, keyword, tags, suggestions_url, session = None):
        # Deferred import to avoid circular dependencies.
        from model.Bookmark import Bookmark
        from model.KeywordBookmark import KeywordBookmark

        if keyword:
            bookmark = KeywordBookmark()
        else:
            bookmark = Bookmark()
        bookmark.fb_user_id = cherrypy.request.fb_user_id
        BookmarkBase.__update(bookmark, name, url, keyword, tags,
                              suggestions_url)
        session.add(bookmark)

    # You need to refetch the bookmark afterwards.
    @with_session(commit = True)
    def update(self, name, url, keyword, tags, suggestions_url, session = None):
        BookmarkBase.__update(self, name, url, keyword, tags,
                              suggestions_url)
        session.add(self)

    @staticmethod
    def __update(bookmark, name, url, keyword, tags, suggestions_url):
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
