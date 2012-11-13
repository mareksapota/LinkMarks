from model.Base import Base
from model.Bookmark import Bookmark
from model.Token import Token

from sqlalchemy import create_engine
engine = create_engine("sqlite:///db.sqlite3", echo = False)
Base.metadata.create_all(engine)
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
