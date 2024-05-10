from sqlalchemy import Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
     
class Address(Base):
    __tablename__ = 'addresses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    
