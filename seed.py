# seed.py
from src.database import SessionLocal, engine, Base
from src.models import Level, Lesson, Exercise

mock_levels_data = [
    {
        "level_code": "A1", 
        "title": "Beginner", 
        "description": "Essential foundations of English",
        "lessons": [
            { 
                "number": 1, "title": 'Introduction to Nouns',
                "exercises": [
                    {
                        "exercise_type": "quiz",
                        "data": { "instruction": "Select the noun in the following sentence: 'The dog barks.'", "options": ["The", "dog", "barks"], "answer": "dog", "xp": 10 }
                    },
                    {
                        "exercise_type": "writing",
                        "data": { "instruction": "Write a short sentence using the noun 'cat'.", "xp": 25 }
                    },
                    {
                        "exercise_type": "speaking",
                        "data": {
                            "instruction": "Click the microphone and read the following sentence out loud:",
                            "sentence_to_read": "The cat sleeps on the mat.",
                            "xp": 35
                        }
                    }
                ]
            },
        ]
    },
    {
        "level_code": "A2", "title": "Elementary", "description": "Build upon your basic knowledge",
        "lessons": [
            { 
                "number": 1, "title": 'Quantifiers',
                "exercises": [
                    {
                        "exercise_type": "quiz",
                        "data": { "instruction": "Which quantifier fits best? 'There isn't _____ milk left.'", "options": ["much", "many", "a lot"], "answer": "much", "xp": 10 }
                    },
                    {
                        "exercise_type": "listening",
                        "data": {
                            "instruction": "Listen to the conversation and answer the question.",
                            "audio_url": "https://cdn.pixabay.com/audio/2022/03/10/audio_285a1a1362.mp3",
                            "question": "What does the woman want to buy?",
                            "options": ["A train ticket", "A bus ticket", "A plane ticket"],
                            "answer": "A train ticket",
                            "xp": 30
                        }
                    }
                ]
            },
        ]
    }
]

def seed_database():
    db = SessionLocal()
    if db.query(Level).count() == 0:
        print("Base de datos vacía. Poblando con datos iniciales...")
        for level_data in mock_levels_data:
            level = Level(
                level_code=level_data["level_code"],
                title=level_data["title"],
                description=level_data["description"]
            )
            for lesson_data in level_data["lessons"]:
                lesson = Lesson(
                    number=lesson_data["number"],
                    title=lesson_data["title"]
                )
                for exercise_data in lesson_data["exercises"]:
                    exercise = Exercise(
                        exercise_type=exercise_data["exercise_type"],
                        data=exercise_data["data"]
                    )
                    lesson.exercises.append(exercise)
                level.lessons.append(lesson)
            db.add(level)
        db.commit()
        print("¡Datos insertados con éxito!")
    else:
        print("La base de datos ya contiene datos. No se realizó ninguna acción.")
    db.close()

if __name__ == "__main__":
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")
    seed_database()