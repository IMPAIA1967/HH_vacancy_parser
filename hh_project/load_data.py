import psycopg2
from api_hh import get_companies_and_vacancies
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def save_companies_and_vacancies():
    """Сохраняет компании и вакансии в БД"""


def save_to_db():
    """Сохраняем компании и вакансии в БД"""
    data = get_companies_and_vacancies()  # получили с hh.ru

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    # Проходим по каждой компании
    for company in data:
        name = company["company_name"]
        hh_id = company["employer_id"]

        # 1. Сохраняем компанию
        cursor.execute(
            "INSERT INTO companies (name, hh_id) VALUES (%s, %s) RETURNING id",
            (name, hh_id)
        )
        company_id = cursor.fetchone()[0]  # id из БД

        # 2. Сохраняем вакансии
        for vac in company["vacancies"]:
            title = vac["name"]
            link = vac["alternate_url"]

            salary = vac.get("salary")  # может быть None
            salary_from = salary["from"] if salary else None
            salary_to = salary["to"] if salary else None
            currency = salary["currency"] if salary else None

            cursor.execute(
                """INSERT INTO vacancies 
                   (name, salary_from, salary_to, currency, url, company_id)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (title, salary_from, salary_to, currency, link, company_id)
            )

    conn.commit()
    cursor.close()
    conn.close()
    print("Всё сохранено!")

if __name__ == "__main__":
    save_to_db()