from sqlalchemy import Sequence, Column
from sqlalchemy import Integer
from sqlalchemy import func

from model.Base import Base
import model

import sys

class SchemaVersion(Base):
    __tablename__ = "schema_version"

    version = Column(Integer, primary_key = True)

    CURRENT_VERSION = 2

    @staticmethod
    def get_version():
        session = model.Session()
        version = session.query(func.max(SchemaVersion.version)).one()[0]
        if version is None:
            version = 0
        return version

    @staticmethod
    def check_version():
        version = SchemaVersion.get_version()
        if version > SchemaVersion.CURRENT_VERSION:
            print("Schema version too high, LinkMarks is probably too old.")
            sys.exit(0)
        if version == SchemaVersion.CURRENT_VERSION:
            return
        if version < SchemaVersion.CURRENT_VERSION:
            print("Schema version too low, use `./upgradeschema.py` or")
            print("`./markschema.py` if this is a new installation.")
            sys.exit(0)

    @staticmethod
    def upgrade():
        version = SchemaVersion.get_version()
        if version < 1:
            session = model.Session()
            session.execute("ALTER TABLE bookmarks ADD COLUMN suggestions_url VARCHAR")
            sv = SchemaVersion()
            sv.version = 1
            session.add(sv)
            session.commit()
        if version < 2:
            session = model.Session()
            session.execute("DROP TABLE tokens")
            session.execute("ALTER TABLE bookmarks ADD COLUMN fb_user_id "
                            "INTEGER NOT NULL DEFAULT 0")
            print("You have to run `UPDATE bookmarks SET fb_user_id = X` "
                  "manually.")
            sv = SchemaVersion()
            sv.version = 2
            session.add(sv)
            session.commit()

    @staticmethod
    def mark():
        version = SchemaVersion.get_version()
        if version < SchemaVersion.CURRENT_VERSION:
            session = model.Session()
            sv = SchemaVersion()
            sv.version = SchemaVersion.CURRENT_VERSION
            session.add(sv)
            session.commit()
