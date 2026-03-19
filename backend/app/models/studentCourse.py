from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class StudentCourse(Base):
    __tablename__ = "student_courses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    status = Column(String, nullable=False)  # approved, failed, in_progress, pending
    grade = Column(Float, nullable=True)
    year = Column(Integer, nullable=True)
    period = Column(Integer, nullable=True)

    student = relationship("Student", back_populates="student_courses")
    course = relationship("Course", back_populates="student_courses")