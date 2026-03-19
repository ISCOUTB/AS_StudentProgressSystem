from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    semester = relationship("Semester", back_populates="courses")
    prerequisites = relationship(
        "Prerequisite",
        foreign_keys="Prerequisite.course_id",
        back_populates="course"
    )
    required_by = relationship(
        "Prerequisite",
        foreign_keys="Prerequisite.required_course_id",
        back_populates="required_course"
    )
    student_courses = relationship("StudentCourse", back_populates="course")