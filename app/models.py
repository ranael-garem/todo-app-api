from database import Base
from helpers import utc_datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)

    description = Column(String)
    completed = Column(Boolean, default=False)
    deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=utc_datetime, nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=utc_datetime,
        onupdate=utc_datetime,
        nullable=False,
    )
    deleted_at = Column(DateTime(timezone=True), nullable=True)
