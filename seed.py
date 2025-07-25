# seed.py
from src.database import SessionLocal, engine, Base
from src.models import Level, Lesson, Exercise

mock_levels_data = [
    {
        "level_code": "A1", "title": "Beginner", "description": "Essential foundations of English",
        "lessons": [
            { 
                "number": 1, "title": 'Introduction to Nouns',
                "exercises": [
                    {
                        "exercise_type": "quiz",
                        "data": {
                            "instruction": "Select the noun in the following sentence: 'The dog barks.'",
                            "options": ["The", "dog", "barks"],
                            "answer": "dog",
                            "xp": 10
                        }
                    },
                    # --- NUEVO EJERCICIO DE ESCRITURA ---
                    {
                        "exercise_type": "writing",
                        "data": {
                            "instruction": "Write a short sentence using the noun 'cat'.",
                            "xp": 25
                        }
                    }
                ]
            },
        ]
    },
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