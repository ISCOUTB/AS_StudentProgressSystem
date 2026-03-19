from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Semester(Base):
    __tablename__ = "semesters"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    number = Column(Integer, nullable=False)
    name = Column(String, nullable=True)

    program = relationship("Program", back_populates="semesters")
    courses = relationship("Course", back_populates="semester")