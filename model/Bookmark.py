from sqlalchemy import Sequence, Column
from sqlalchemy import Integer, String
from sqlalchemy import or_

from model.Base import Base
import model

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
    def find_all(query):
        like_query = "%{0}%".format(query)
        session = model.Session()
        return session.query(Bookmark).filter(or_(
            Bookmark.name.like(like_query),
            Bookmark.url.like(like_query),
            Bookmark.keyword.like(like_query)
        )).order_by(
            Bookmark.name
        ).order_by(
            Bookmark.id
        ).all()

    @staticmethod
    def new(name, url, keyword):
        session = model.Session()
        bookmark = Bookmark()
        bookmark.name = name
        bookmark.url = url
        if keyword:
            bookmark.keyword = keyword
        else:
            bookmark.keyword = None
        session.add(bookmark)
        session.commit()

    @staticmethod
    def update(id, name, url, keyword):
        bookmark = Bookmark.get(id)
        session = model.Session()
        bookmark.name = name
        bookmark.url = url
        bookmark.keyword = keyword
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

    def search(self, query):
        query = query[len(self.keyword) + 1:]
        url = self.url.replace("%s", query)
        return url
