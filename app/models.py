from sqlalchemy.sql.expression import null, text
from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from .database import Base

__name__ = "models"

class Post(Base):
    __tablename__ = "postsv3"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    
