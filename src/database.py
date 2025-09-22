import psycopg2


DB_NAME = "hh_vacancies"
DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"


def get_connection(dbname=DB_NAME) -> psycopg2.connect:
    """Создает подключение к БД"""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            client_encoding='utf-8'
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None


def create_database() -> None:
    """ Создаем базу данных """
    # Подключаемся к стандартной БД, чтобы создать новую
    conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cur = conn.cursor()

    # Проверяем, есть ли уже такая БД, и если нет - создаем
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"База данных {DB_NAME} создана.")
    else:
        print(f"База данных {DB_NAME} уже существует.")

    cur.close()
    conn.close()


def create_tables() -> None:
    """
    Создает таблицы в базе данных.
    """
    # Подключаемся к нашей созданной БД
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # SQL-команда для создания таблицы компаний
    create_employers_table = """
    CREATE TABLE IF NOT EXISTS employers (
        employer_id VARCHAR(20) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        url TEXT
    )
"""

    # SQL-команда для создания таблицы вакансий
    create_vacancies_table = """
    CREATE TABLE IF NOT EXISTS vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        employer_id VARCHAR(20) REFERENCES employers(employer_id) ON DELETE CASCADE,
        title VARCHAR(100) NOT NULL,
        salary_from INTEGER,
        salary_to INTEGER,
        url TEXT,
        description TEXT
    )
"""
    # Выполняем наши команды
    cur.execute(create_employers_table)
    cur.execute(create_vacancies_table)

    # Сохраняем изменения в БД
    conn.commit()

    cur.close()
    conn.close()
    print("Таблицы созданы успешно.")


def insert_employer_data(conn, employer_data) -> None:
    """
    Вставляет данные о компании в таблицу employers
    """
    cur = conn.cursor()
    # SQL-запрос для вставки данных. %s - это placeholder для наших значений
    query = """
        INSERT INTO employers (employer_id, name, url)
        VALUES (%s, %s, %s)
        ON CONFLICT (employer_id) DO NOTHING
    """
    # Подставляем значения из словаря в наш запрос
    cur.execute(query, (employer_data['id'], employer_data['name'], employer_data['url']))
    conn.commit()  # Сохраняем изменения
    cur.close()


def insert_vacancy_data(conn, vacancy_data) -> None:
    """
    Вставляет данные о вакансии в таблицу vacancies.
    """
    cur = conn.cursor()
    query = """
        INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    cur.execute(query, (
        vacancy_data['employer_id'],
        vacancy_data['name'],
        vacancy_data['salary_from'],
        vacancy_data['salary_to'],
        vacancy_data['url'],
        vacancy_data['description']
    ))
    conn.commit()
    cur.close()
