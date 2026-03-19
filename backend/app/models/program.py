from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    faculty = Column(String, nullable=False)
    total_credits = Column(Integer, nullable=False)

    semesters = relationship("Semester", back_populates="program")
    students = relationship("Student", back_populates="program")
    achievements = relationship("Achievement", back_populates="program")