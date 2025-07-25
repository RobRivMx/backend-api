# src/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Level(Base):
    __tablename__ = "levels"
    id = Column(Integer, primary_key=True, index=True)
    level_code = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    lessons = relationship("Lesson", back_populates="owner_level")

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    number = Column(Integer)
    level_id = Column(Integer, ForeignKey("levels.id"))
    owner_level = relationship("Level", back_populates="lessons")
    # Nueva relación: una lección ahora tiene muchos ejercicios
    exercises = relationship("Exercise", back_populates="owner_lesson")

class Exercise(Base):
    __tablename__ = "exercises"
    id = Column(Integer, primary_key=True, index=True)
    exercise_type = Column(String) # 'quiz', 'fill_in_the_blank', etc.
    # Usamos JSON para guardar la data del ejercicio (preguntas, opciones, respuestas)
    data = Column(JSON)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    owner_lesson = relationship("Lesson", back_populates="exercises")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    xp = Column(Integer, default=0) # <--- AÑADE ESTA LÍNEA

