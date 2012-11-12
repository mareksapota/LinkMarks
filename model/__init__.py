from Base import Base
from Bookmark import Bookmark
from Token import Token

from sqlalchemy import create_engine
engine = create_engine("sqlite:///db.sqlite3", echo = False)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
