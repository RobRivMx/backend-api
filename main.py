# main.py
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
import google.generativeai as genai
from dotenv import load_dotenv

from src import models, schemas
from src.database import engine, get_db

# --- CONFIGURACIÓN INICIAL ---
load_dotenv()
models.Base.metadata.create_all(bind=engine)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No se encontró la GEMINI_API_KEY. Asegúrate de que tu archivo .env es correcto.")
genai.configure(api_key=GEMINI_API_KEY)

# --- CONFIGURACIÓN DE SEGURIDAD ---
SECRET_KEY = "tu-super-secreto-y-dificil-de-adivinar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# --- CONFIGURACIÓN DE CORS ---
origins = ["http://localhost:5173", "http://localhost:5174"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- LÓGICA DE CONTRASEÑAS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# --- LÓGICA DE TOKENS (JWT) ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- FUNCIÓN PARA OBTENER EL USUARIO ACTUAL ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- ENDPOINTS DE LA API ---

@app.get("/api/levels", response_model=List[schemas.Level])
def get_levels(db: Session = Depends(get_db)):
    levels = db.query(models.Level).options(joinedload(models.Level.lessons)).all()
    return levels

@app.get("/api/lessons/{lesson_id}", response_model=schemas.LessonDetail)
def get_lesson_by_id(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(models.Lesson).options(joinedload(models.Lesson.exercises)).filter(models.Lesson.id == lesson_id).first()
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return lesson

@app.post("/register", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.post("/api/progress/correct_answer", response_model=schemas.User)
def record_correct_answer(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.xp += 10
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/api/tutor/chat", response_model=schemas.ChatResponse)
def chat_with_tutor(user_message: schemas.ChatMessage, current_user: models.User = Depends(get_current_user)):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(user_message.message)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/writing/feedback", response_model=schemas.WritingFeedback)
def get_writing_feedback(submission: schemas.WritingSubmission, current_user: models.User = Depends(get_current_user)):
    prompt_template = f"""
    Eres un tutor de inglés amigable y experto llamado Spacy. Un estudiante ha escrito un texto basado en la siguiente instrucción: "{submission.prompt}". El texto del estudiante es: "{submission.text}".
    Por favor, evalúa el texto y responde EXACTAMENTE en el siguiente formato JSON:
    {{
        "correction": "[Aquí escribe el texto del estudiante con las correcciones en mayúsculas. Si no hay errores, repite el texto original]",
        "feedback": "[Aquí escribe un comentario corto, positivo y útil en español sobre el texto.]",
        "score": [Aquí escribe un número del 1 al 5, donde 5 es excelente.]
    }}
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt_template)
        # Limpiamos y parseamos la respuesta JSON de la IA
        import json
        clean_response = response.text.strip().replace("```json", "").replace("```", "")
        feedback_data = json.loads(clean_response)
        return feedback_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contactar o procesar la IA: {str(e)}")

# --- ENDPOINTS PARA HERRAMIENTAS DE ESCRITURA CON IA ---
@app.post("/api/writing/grammar_check", response_model=schemas.ToolResponse)
def grammar_check(submission: schemas.WritingSubmission, current_user: models.User = Depends(get_current_user)):
    prompt = f"""Actúa como un corrector de gramática. Corrige el siguiente texto y devuelve únicamente el texto corregido.\nTexto del estudiante: "{submission.text}" """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/writing/verb_suggestions", response_model=schemas.ToolResponse)
def get_verb_suggestions(request: schemas.ToolRequest, current_user: models.User = Depends(get_current_user)):
    prompt = f"""Actúa como un profesor de inglés. Para el tema "{request.prompt}", sugiere 5 verbos útiles en inglés, separados por comas. Devuelve solo los verbos."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/writing/example", response_model=schemas.ToolResponse)
def get_example(request: schemas.ToolRequest, current_user: models.User = Depends(get_current_user)):
    prompt = f"""Actúa como un profesor de inglés. Escribe una oración de ejemplo, simple y corta, para un estudiante de nivel A1 sobre el tema: "{request.prompt}". Devuelve solo la oración."""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINT PARA SPACY DENTRO DE LA LECCIÓN ---
@app.post("/api/lessons/chat", response_model=schemas.ChatResponse)
def lesson_chat_with_tutor(request: schemas.InLessonChatRequest, current_user: models.User = Depends(get_current_user)):
    system_prompt = ""
    if request.mode == "practice":
        system_prompt = f"Actúa como un compañero de conversación para practicar inglés llamado Spacy. El usuario es un estudiante y quiere practicar el tema: '{request.lesson_topic}'. Inicia una conversación de role-playing simple y corta sobre ese tema. Haz preguntas sencillas para que el usuario pueda responder. Mantén tus respuestas cortas y amigables."
    elif request.mode == "question":
        system_prompt = f"Actúa como un profesor de inglés experto y amigable llamado Spacy. El usuario está estudiando el tema '{request.lesson_topic}' y tiene una pregunta. Responde su pregunta de forma clara y concisa, enfocándote únicamente en el tema de la lección. Usa ejemplos si es necesario. Responde en español si la pregunta es en español."

    full_prompt = f"{system_prompt}\n\nMensaje del usuario: \"{request.message}\""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(full_prompt)
        return {"reply": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al contactar la IA: {str(e)}")