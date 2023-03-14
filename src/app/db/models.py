from .session import Base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
)


class User(Base):
    email = Column(String(length=255), unique=True, nullable=False)
    first_name = Column(String(length=255))
    last_name = Column(String(length=255))
    password = Column(String(length=255))
    is_disabled = Column(Boolean, default=False)
    reset_token = Column(String(length=255))
    scopes = Column(String(length=255))
    last_login = Column(DateTime)


# TODO: consider an user access / settings object to enable users for api & model access
