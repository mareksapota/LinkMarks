from model.Base import Base
from model.BookmarkBase import BookmarkBase
from model.Bookmark import Bookmark
from model.KeywordBookmark import KeywordBookmark
from model.SchemaVersion import SchemaVersion

from sqlalchemy import create_engine
engine = create_engine("sqlite:///db.sqlite3", echo = False)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
