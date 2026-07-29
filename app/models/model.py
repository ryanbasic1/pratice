from sqlalchemy import Column, Integer, String,ForeignKey, UniqueConstraint
from app.database  import Base

class User(Base):
    __tablename__ = "users"
    display_name = Column(String,unique=True, index=True )
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    
    user_id = Column(Integer,ForeignKey("users.id"))

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id",ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "note_id", name="unique_like"),
    )