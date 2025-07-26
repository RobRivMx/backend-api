# src/schemas.py
from pydantic import BaseModel
from typing import List, Any

# --- Schemas de Ejercicios ---
class Exercise(BaseModel):
    id: int
    exercise_type: str
    data: Any
    class Config: from_attributes = True

# --- Schemas de Lecciones ---
class LessonSummary(BaseModel):
    id: int
    number: int
    title: str
    class Config: from_attributes = True

class LessonDetail(LessonSummary):
    exercises: List[Exercise] = []
    class Config: from_attributes = True

# --- Schema de Nivel ---
class Level(BaseModel):
    level_code: str
    title: str
    description: str
    lessons: List[LessonSummary] = []
    class Config: from_attributes = True

# --- Schemas de Usuario ---
class UserCreate(BaseModel):
    email: str
    password: str

class User(BaseModel):
    id: int
    email: str
    xp: int
    class Config: from_attributes = True

# --- Schemas de Token y Chat ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --- SCHEMAS PARA HERRAMIENTAS DE ESCRITURA ---
class WritingSubmission(BaseModel):
    text: str
    prompt: str

class WritingFeedback(BaseModel):
    correction: str
    feedback: str
    score: int

class ToolRequest(BaseModel):
    prompt: str

class ToolResponse(BaseModel):
    result: str

    # Al final de src/schemas.py
class TranscriptionResponse(BaseModel):
    transcript: str

class InLessonChatRequest(BaseModel):
    message: str
    lesson_topic: str
    mode: str # "practice" o "question"