from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Prerequisite(Base):
    __tablename__ = "prerequisites"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    required_course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)

    course = relationship(
        "Course",
        foreign_keys=[course_id],
        back_populates="prerequisites"
    )
    required_course = relationship(
        "Course",
        foreign_keys=[required_course_id],
        back_populates="required_by"
    )