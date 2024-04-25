from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, Integer, String,Column, Text, null, text
from .database import Base
from sqlalchemy.orm import relationship

## python knows table name 'Post', need to translate to postgres
## these are sqlalchemy models
class Post(Base):
    __tablename__ ="posts"
    id = Column(Integer,primary_key = True, nullable = False)
    title= Column(String,nullable = False)
    content = Column(String,nullable = False)
    published = Column(Boolean,server_default = 'TRUE',nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default=text('Now()'))
    rating  = Column(Integer,nullable = True,server_default='0')
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    ##basically the relationship figures out whats the relation between Post model and user model
    ## so owner will get populated as owner = {id,email,password,created_at}

class User(Base):
    __tablename__ ="users"
    id = Column(Integer,nullable=False,primary_key=True)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable = False,server_default= text('now()'))
    phone_number = Column(String)

class Vote(Base):
    __tablename__ ="votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable = False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable = False,primary_key=True)
    
    
    
    
    
    