from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    mobile = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    # owner | milkman
    role = Column(String, default="milkman")
    # If milkman → owner_id = owner.id
    # If owner → NULL (or self-id if also milkman)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    language = Column(String, default="ta")
    is_active = Column(Boolean, default=True)