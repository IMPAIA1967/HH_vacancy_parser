import psycopg2

from api_hh import get_employer_data, get_vacancies_data
from database import create_database, create_tables, insert_employer_data, insert_vacancy_data
from db_manager import DBManager



COMPANY_IDS = ['15478',  # VK
               '1740',   # Яндекс
               '3529',   # Сбер
               '4181',   # Тинькофф
               '78638',  # Тинькофф
               '2748',   # Ростелеком
               '3127',   # МТС
               '3776',   # МегаФон
               '907345', # Ozon
               '2180']   # Лаборатория Касперского

def main():
    """
    Основная функция проекта. Здесь все собирается воедино
    """
    print("Создаем базу данных и таблицы...")
    create_database()
    create_tables()

    # Подключаемся к нашей БД для заполнения данными
    conn = psycopg2.connect(dbname="hh_vacancies", user="postgres", password="12345", host="localhost", port="5432")

    print("Начинаем сбор данных с HH.ru...")
    for company_id in COMPANY_IDS:
        print(f"Обрабатываем компанию с ID: {company_id}")
        # Получаем данные о компании
        employer = get_employer_data(company_id)
        insert_employer_data(conn, employer)

        # Получаем вакансии для этой компании
        vacancies = get_vacancies_data(company_id)
        for vac in vacancies:
            insert_vacancy_data(conn, vac)  # Сохраняем каждую вакансию в БД
        print(f"Добавлено вакансий: {len(vacancies)} для {employer['name']}")

    conn.close()  # Закрываем соединение после записи всех данных
    print("Данные успешно загружены в БД!")

    # Теперь работаем с менеджером БД
    db_manager = DBManager("hh_vacancies", "postgres", "12345", "localhost", "5432")

    # Бесконечный цикл для меню
    while True:
        print("\n--- Что вы хотите сделать? ---")
        print("1. Показать список компаний и количество вакансий")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выйти")

        choice = input("Ваш выбор: ")

        if choice == "1":
            data = db_manager.get_companies_and_vacancies_count()
            for company, count in data:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            data = db_manager.get_all_vacancies()
            for company, title, salary_from, salary_to, url in data:
                salary_info = f"от {salary_from}" if salary_from else "не указана"
                if salary_to:
                    salary_info += f" до {salary_to}"
                print(f"{company} - {title} - Зарплата: {salary_info} - {url}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по вакансиям: {avg_salary} руб.")

        elif choice == "4":
            data = db_manager.get_vacancies_with_higher_salary()
            for vac in data:
                # vac - это кортеж, элементы соответствуют столбцам в таблице vacancies
                print(f"{vac[2]} (ID: {vac[0]}) - Зарплата от: {vac[3]} - {vac[5]}")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ")
            data = db_manager.get_vacancies_with_keyword(keyword)
            for vac in data:
                print(f"{vac[2]} - {vac[5]}")

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный ввод, попробуйте еще раз.")


if __name__ == "__main__":
    main()