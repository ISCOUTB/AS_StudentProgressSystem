from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    student_code = Column(String, unique=True, nullable=False)
    admission_year = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="students")
    student_courses = relationship("StudentCourse", back_populates="student")
    student_achievements = relationship("StudentAchievement", back_populates="student")