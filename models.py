from sqlalchemy import Boolean, Column, Integer, String, Float
from database import base


class User(base):
    __tablename__ = "apiusrs"
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(250), unique=True, primary_key=True, index=True)
    password = Column(String(250), nullable=False)

    # Additional user information
    body_weight = Column(Float, nullable=True)  # Weight in kilograms 
    height = Column(Float, nullable=True)  # Height in centimeters
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)  # 'Male', 'Female', etc
