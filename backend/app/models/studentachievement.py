from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class StudentAchievement(Base):
    __tablename__ = "student_achievements"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)
    earned_at = Column(Date, nullable=False)

    student = relationship("Student", back_populates="student_achievements")
    achievement = relationship("Achievement", back_populates="student_achievements")