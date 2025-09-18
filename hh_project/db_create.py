# db_create.py
import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def create_database():
    """Создаёт Базу данных hh_db, если её ещё нет"""
    conn = psycopg2.connect(
        dbname="postgres",  # подключаемся к стандартной БД
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Проверяем, есть ли уже БД
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"✅ База данных '{DB_NAME}' создана")
    else:
        print(f"ℹ️ База данных '{DB_NAME}' уже существует")

    cursor.close()
    conn.close()

def create_tables():
    """Создаёт таблицы companies и vacancies"""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Таблица компаний
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            hh_id INTEGER UNIQUE
        );
    """)

    # Таблица вакансий
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(10),
            url TEXT,
            company_id INTEGER REFERENCES companies(id)
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Таблицы созданы (или уже были)")

if __name__ == "__main__":
    create_database()
    create_tables()