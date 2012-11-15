from sqlalchemy import Sequence, Column
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy import and_

from model.Base import Base
import model

import os
import base64
from datetime import datetime, timedelta

class Token(Base):
    __tablename__ = "tokens"

    id = Column(
        Integer,
        Sequence("tokens_id_seq"),
        primary_key = True
    )

    value = Column(String, nullable = False)
    permanent = Column(Boolean, nullable = False)
    issue_time = Column(DateTime, nullable = False)

    @staticmethod
    def issue():
        session = model.Session()
        token = Token()
        token.value = base64.urlsafe_b64encode(os.urandom(128)).decode()
        token.permanent = False
        token.issue_time = datetime.now()
        session.add(token)
        session.commit()
        return token.value

    @staticmethod
    def save(value, permanent):
        session = model.Session()
        token = Token()
        token.value = value
        token.permanent = permanent
        token.issue_time = datetime.now()
        session.add(token)
        session.commit()

    @staticmethod
    def use(value):
        Token.clean()
        session = model.Session()
        token = session.query(Token).filter(Token.value == value).first()
        if not token.permanent:
            session.delete(token)
        session.commit()

    @staticmethod
    def clean():
        old = datetime.now() - timedelta(hours = 1)
        session = model.Session()
        stale = session.query(Token).filter(and_(
            Token.issue_time <= old,
            Token.permanent == False
        )).all()
        map(session.delete, stale)
        session.commit()
