# seed.py
from src.database import SessionLocal, engine, Base
from src.models import Level, Lesson, Exercise

# TEMARIO COMPLETO CON LA PRIMERA LECCIÓN DETALLADA
mock_levels_data = [
    {
        "level_code": "A1", "title": "Básico", "description": "Fundamentos esenciales del inglés.",
        "lessons": [
            {
                "number": 1, "title": "Greetings and Introductions",
                "exercises": [
                    {
                        "exercise_type": "grammar_notes",
                        "data": {
                            "title": "Saludos y Presentaciones",
                            "points": [
                                {"header": "¿Para qué sirve?", "content": "Los saludos ('Greetings') son la primera palabra en cualquier conversación. Son la clave para iniciar una interacción de forma amigable."},
                                {"header": "Las Estructuras Clave", "content": "Formales (trabajo, desconocidos): Good morning, Good afternoon, Hello, my name is...\nInformales (amigos, familia): Hi!, Hey!, What's up?"},
                                {"header": "Tip de Spacy 💡", "content": "¡Cuidado con la noche! Usa 'Good evening' para saludar al llegar, y 'Good night' solo para despedirte antes de ir a dormir."}
                            ]
                        }
                    },
                    {
                        "exercise_type": "quiz",
                        "data": {
                            "title": "El Saludo Correcto", "instruction": "Elige la opción correcta para cada situación.", "xp": 10,
                            "questions": [
                                {"id": "q1", "question": "Llegas a una reunión de trabajo a las 10 AM. ¿Cómo saludas?", "options": ["What's up?", "Good morning.", "Good night."], "answer": "Good morning."},
                                {"id": "q2", "question": "Te encuentras con un amigo en la calle. ¿Qué le dices?", "options": ["Hello, my name is...", "Good afternoon.", "Hey, what's up?"], "answer": "Hey, what's up?"},
                                {"id": "q3", "question": "Te despides de alguien por la noche. ¿Qué dices?", "options": ["Good evening.", "Good night.", "Hello."], "answer": "Good night."}
                            ]
                        }
                    },
                    {
                        "exercise_type": "fill_in_the_blank",
                        "data": { "title": "Completa la Presentación", "instruction": "Rellena el espacio para completar la presentación.", "xp": 10, "sentences": [{"id": "s1", "start": "Hello, my name ___ Spacy.", "end": "", "answer": "is"}] }
                    },
                    {
                        "exercise_type": "matching",
                        "data": {
                            "title": "Une el Saludo con su Significado", "instruction": "Arrastra el saludo informal a su equivalente más formal.", "xp": 15,
                            "pairs": [{"id": "word1", "content": "Hi!"}, {"id": "word2", "content": "What's up?"}, {"id": "word3", "content": "Bye!"}],
                            "matches": [{"id": "match1", "content": "How are you?"}, {"id": "match2", "content": "Goodbye."}, {"id": "match3", "content": "Hello."}],
                            "solution": { "word1": "match3", "word2": "match1", "word3": "match2" }
                        }
                    },
                    {
                        "exercise_type": "listening",
                        "data": {
                            "title": "Comprensión Auditiva", "instruction": "Escucha la presentación y responde la pregunta.", "xp": 15,
                            "audio_url": "https://storage.googleapis.com/gemini-prod-us-west1-assets/2024/07/26/hello_my_name_is_anna.mp3",
                            "question": "What is her name?", "options": ["Emma", "Anna", "Amy"], "answer": "Anna"
                        }
                    },
                    {
                        "exercise_type": "pronunciation",
                        "data": { "title": "Práctica de Pronunciación", "instruction": "Escucha y luego practica diciendo la palabra.", "word": "Hello", "phonetic": "/həˈloʊ/", "xp": 20 }
                    },
                    {
                        "exercise_type": "error_detection",
                        "data": {
                            "title": "Detecta el Error", "instruction": "La siguiente frase, ¿es correcta o incorrecta?", "xp": 15,
                            "sentence": "I name is Peter.", "options": ["Correct", "Incorrect"], "answer": "Incorrect", "explanation": "La forma correcta es 'My name is Peter'."
                        }
                    },
                    {
                        "exercise_type": "reading",
                        "data": {
                            "title": "Mini Diálogo", "instruction": "Lee la conversación y responde la pregunta.", "xp": 10,
                            "text": "A: Hello, I'm Maria.\nB: Hi Maria, I'm David. Nice to meet you.\nA: Nice to meet you too, David.",
                            "comprehension_quiz": {"questions": [{"id": "q1", "question": "What is the man's name?", "options": ["Peter", "Maria", "David"], "answer": "David"}]}
                        }
                    },
                    {
                        "exercise_type": "writing",
                        "data": { "title": "¡Tu Turno!", "instruction": "Preséntate en una oración simple en inglés.", "xp": 25 }
                    },
                    {
                        "exercise_type": "speaking",
                        "data": { "title": "Práctica de Speaking", "instruction": "Haz clic en el micrófono y preséntate en voz alta.", "sentence_to_read": "Hello, my name is...", "xp": 35 }
                    }
                ]
            },
            # Lecciones restantes del A1 con placeholders
            {"number": 2, "title": "Adjectives (Introduction)"},
            {"number": 2, "title": "Nouns (Introduction)"},
            {"number": 3, "title": "Plural Nouns"},
            {"number": 4, "title": "Articles (a, an, the)"},
            {"number": 5, "title": "Pronouns (Introduction)"},
            {"number": 6, "title": "Subject & Object Pronouns"},
            {"number": 7, "title": "Possessive Adjectives and Pronouns"},
            {"number": 8, "title": "Demonstratives (this, that, these, those)"},
            {"number": 9, "title": "Basic Adjectives"},
            {"number": 10, "title": "Adverbs (Introduction)"},
            {"number": 11, "title": "Frequency Adverbs"},
            {"number": 12, "title": "Prepositions of Place and Time"},
            {"number": 13, "title": "Conjunctions (and, but, or)"},
            {"number": 14, "title": "Verbs (Introduction)"},
            {"number": 15, "title": "The Verb 'To Be' (Present Simple)"},
            {"number": 16, "title": "Simple Present"},
            {"number": 17, "title": "Introduction to Auxiliary Verbs"},
            {"number": 18, "title": "Simple Past (Verb To Be & Regular Verbs)"},
            {"number": 19, "title": "Simple Future (will / be going to - basic)"},
            {"number": 20, "title": "Questions (General Introduction)"},
            {"number": 21, "title": "Wh-Words (Who, What, Where, When, Why, How)"},
            {"number": 22, "title": "There is / There are"},
            {"number": 23, "title": "Countable and Uncountable Nouns (basic)"},
            {"number": 24, "title": "Imperatives"},
            {"number": 25, "title": "Numbers (0-100)"},
            {"number": 26, "title": "Colors"},
            {"number": 27, "title": "Days of the Week"},
            {"number": 28, "title": "Months of the Year"},
            {"number": 29, "title": "Seasons"},
        ]
    },
    {
        "level_code": "A2", "title": "Básico Avanzado", "description": "Construye sobre tus conocimientos básicos.",
        "lessons": [
            {"number": 1, "title": "Review of A1 Essentials"},
            {"number": 2, "title": "Present Continuous / Progressive"},
            {"number": 3, "title": "Past Simple (Regular & Irregular Verbs)"},
            {"number": 4, "title": "Future Forms (will & be going to)"},
            {"number": 5, "title": "Modal Verbs (Can, Could, Must, Have to, Should)"},
            {"number": 6, "title": "Quantifiers (much, many, some, any)"},
            {"number": 7, "title": "Comparatives & Superlatives"},
            {"number": 8, "title": "Possessive Adjectives vs. Possessive Pronouns"},
            {"number": 9, "title": "Zero Conditional"},
            {"number": 10, "title": "First Conditional (Introduction)"},
            {"number": 11, "title": "Adverbs of Manner"},
            {"number": 12, "title": "Prepositions of Movement"},
            {"number": 13, "title": "Time Clauses (When, While, Before, After)"},
            {"number": 14, "title": "'Too' and 'Enough'"},
            {"number": 15, "title": "'Used to'"},
            {"number": 16, "title": "Basic Phrasal Verbs"},
            {"number": 17, "title": "Connecting Words (Basic-Intermediate)"},
            {"number": 18, "title": "Functional Language: Asking for/Giving Directions"},
        ]
    },
    {
        "level_code": "B1", "title": "Intermedio", "description": "Avanza en tus habilidades de comunicación.",
        "lessons": [
            {"number": 1, "title": "Review of A2 Grammar"},
            {"number": 2, "title": "Present Perfect Simple"},
            {"number": 3, "title": "Present Perfect Continuous/Progressive"},
            {"number": 4, "title": "Past Simple vs. Present Perfect"},
            {"number": 5, "title": "Past Progressive"},
            {"number": 6, "title": "Past Perfect Simple (Introduction)"},
            {"number": 7, "title": "Future Continuous / Progressive"},
            {"number": 8, "title": "First Conditional (Consolidation)"},
            {"number": 9, "title": "Second Conditional (Introduction)"},
            {"number": 10, "title": "Relative Pronouns"},
            {"number": 11, "title": "Reflexive Pronouns"},
            {"number": 12, "title": "Tag Questions"},
            {"number": 13, "title": "Passive Voice (Present & Past Simple)"},
            {"number": 14, "title": "Gerunds and Infinitives"},
            {"number": 15, "title": "Modal Verbs for Speculation (Basic)"},
            {"number": 16, "title": "Reported Speech (Statements)"},
            {"number": 17, "title": "Connecting Words (Intermediate-Advanced)"},
            {"number": 18, "title": "Phrasal Verbs (Intermediate)"},
            {"number": 19, "title": "Vocabulary Expansion: Collocations"},
        ]
    },
    {
        "level_code": "B2", "title": "Intermedio Avanzado", "description": "Refina tu fluidez.",
        "lessons": [
            {"number": 1, "title": "Review of B1 Grammar"},
            {"number": 2, "title": "Present Perfect Adverbs"},
            {"number": 3, "title": "Past Perfect Simple & Continuous"},
            {"number": 4, "title": "Future Perfect Simple"},
            {"number": 5, "title": "Future Perfect Continuous"},
            {"number": 6, "title": "Second Conditional (Consolidation)"},
            {"number": 7, "title": "Third Conditional (Introduction)"},
            {"number": 8, "title": "Mixed Conditionals (Introduction)"},
            {"number": 9, "title": "Equatives (As...as)"},
            {"number": 10, "title": "Participle Adjectives (-ing vs. -ed)"},
            {"number": 11, "title": "Active and Passive Voice (All Tenses)"},
            {"number": 12, "title": "Reported Speech (All Forms)"},
            {"number": 13, "title": "Past Modals"},
            {"number": 14, "title": "Causative Form (Have/Get something done)"},
            {"number": 15, "title": "Wish / If Only"},
            {"number": 16, "title": "Unreal Past (Subjunctive-like uses)"},
            {"number": 17, "title": "Inversion (Basic)"},
            {"number": 18, "title": "Advanced Phrasal Verbs & Idioms"},
            {"number": 19, "title": "Connecting Words (Advanced)"},
        ]
    },
    {
        "level_code": "C1", "title": "Avanzado", "description": "Domina un lenguaje complejo.",
        "lessons": [
            {"number": 1, "title": "Review of B2 Grammar & Nuances"},
            {"number": 2, "title": "Past Perfect Progressives (Full Mastery)"},
            {"number": 3, "title": "Future Perfect Continuous (Full Mastery)"},
            {"number": 4, "title": "All Passive Voice Tenses (Full Mastery)"},
            {"number": 5, "title": "Reported Speech (Advanced)"},
            {"number": 6, "title": "Complex Sentence Structures"},
            {"number": 7, "title": "Inversion (Advanced)"},
            {"number": 8, "title": "Cleft Sentences"},
            {"number": 9, "title": "Ellipsis and Substitution"},
            {"number": 10, "title": "Gerunds and Infinitives (Advanced Use)"},
            {"number": 11, "title": "Relative Clauses (Advanced)"},
            {"number": 12, "title": "Determiners (Advanced)"},
            {"number": 13, "title": "Prefixes and Suffixes"},
            {"number": 14, "title": "Advanced Collocations & Idioms"},
            {"number": 15, "title": "Discourse Markers"},
            {"number": 16, "title": "Formal vs. Informal Language"},
            {"number": 17, "title": "Academic Vocabulary"},
        ]
    },
    {
        "level_code": "C2", "title": "Dominio", "description": "Alcanza un dominio similar al nativo.",
        "lessons": [
            {"number": 1, "title": "Mastery of All Verb Tenses"},
            {"number": 2, "title": "Third Conditional (Full Mastery)"},
            {"number": 3, "title": "Future Perfect Progressives (Full Mastery)"},
            {"number": 4, "title": "Embedded Questions (Advanced)"},
            {"number": 5, "title": "Advanced Idioms & Collocations"},
            {"number": 6, "title": "Complex Discourse Cohesion"},
            {"number": 7, "title": "Figurative Language"},
            {"number": 8, "title": "Subjunctive Mood (Advanced Use)"},
            {"number": 9, "title": "Participle Clauses (Advanced)"},
            {"number": 10, "title": "Nominalization"},
            {"number": 11, "title": "Advanced Inversion & Emphasis"},
            {"number": 12, "title": "Less Common Sentence Structures"},
            {"number": 13, "title": "Grammar for Persuasion"},
            {"number": 14, "title": "Vocabulary for Specialized Fields"},
            {"number": 15, "title": "Cultural & Allusive Language"},
        ]
    },
]


def seed_database():
    db = SessionLocal()
    if db.query(Level).count() == 0:
        print("Base de datos vacía. Poblando con temario completo...")
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
                
                if "exercises" in lesson_data:
                    for exercise_data in lesson_data["exercises"]:
                        exercise = Exercise(
                            exercise_type=exercise_data["exercise_type"],
                            data=exercise_data["data"]
                        )
                        lesson.exercises.append(exercise)
                else:
                    exercise = Exercise(
                        exercise_type="quiz",
                        data={ "instruction": f"Este es un ejercicio de placeholder para {lesson_data['title']}.", "options": ["Opción A", "Opción B", "Opción C"], "answer": "Opción A", "xp": 10 }
                    )
                    lesson.exercises.append(exercise)

                level.lessons.append(lesson)
            db.add(level)
        db.commit()
        print("¡Temario completo insertado con éxito!")
    else:
        print("La base de datos ya contiene datos. No se realizó ninguna acción.")
    db.close()

if __name__ == "__main__":
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")
    seed_database()