# app/models/user.py
from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base 

class Auth(Base):
    __tablename__ = "auths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    refresh_token_hash = Column(String, unique=True, index=True, nullable=False)
    expiration_date = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="tokens")
