from sqlalchemy import Column, Integer, String, Boolean , ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

# Post model
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String, nullable=False)  
    published = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    owner = relationship("User")


# User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Votes(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey("users.id",ondelete='CASCADE'),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete='CASCADE'),primary_key=True)
