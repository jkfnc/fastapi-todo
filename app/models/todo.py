from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from app.database.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    date = Column(Date, server_default=func.current_date())
    
    @hybrid_property
    def creation_date(self):
        return self.created_at.date() if self.created_at else None