import os
from contextlib import contextmanager
from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import uuid
from app.config import DB_CONNECTION_STR, TEST_DB_CONNECTION_STR


engine = create_engine(
    DB_CONNECTION_STR, pool_pre_ping=True, pool_size=32, max_overflow=64
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

test_engine = create_engine(TEST_DB_CONNECTION_STR)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    modified_by_id = Column(Integer, nullable=False)
    external_id = Column(String(length=255), index=True, default=uuid.uuid4)
    is_deleted = Column(Boolean, default=False)
    __name__: str
    
    @declared_attr
    def created_by_id(cls):
        return Column('created_by_id', ForeignKey('user.id'))

    @declared_attr
    def created_by(cls):
        return relationship('User', primaryjoin='User.id==%s.created_by_id' % cls.__name__)

    @declared_attr
    def modified_by_id(cls):
        return Column('modified_by_id', ForeignKey('user.id'))

    @declared_attr
    def modified_by(cls):
        return relationship('User', primaryjoin='User.id==%s.modified_by_id' % cls.__name__)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Base = declarative_base(cls=Base)


@contextmanager
def SessionManager():
    is_test = os.environ.get("TEST_RUN")
    db = TestingSessionLocal() if is_test else SessionLocal()
    try:
        yield db
    finally:
        db.close()
