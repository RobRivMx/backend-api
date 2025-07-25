import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

print("Intentando conectar a la base de datos...")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ ¡Conexión a Neon exitosa!")
    conn.close()
except Exception as e:
    print("❌ Error al conectar:")
    print(e)