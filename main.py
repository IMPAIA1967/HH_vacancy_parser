from src.hh_api import HHApi
from src.database import DatabaseManager
from src.db_manager import DBManager
import time


COMPANY_IDS = [
    "1740",   # Яндекс
    "87021",  # Wildberries
    "3529",   # Сбер
    "2180",   # Ozon
    "4181",   # VK
    "78638",  # Тинькофф
    "3776",   # МТС
    "15478",  # VK Company
    "64174",  # Avito
    "3127",   # Билайн
]

def main():
    print("🚀 Запуск проекта по сбору вакансий с hh.ru")

    # Шаг 1: Создание БД и таблиц
    print("🔧 Создание базы данных...")
    DatabaseManager.create_database()

    print("🔧 Создание таблиц...")
    DatabaseManager.create_tables()

    # Шаг 2: Сбор данных через API
    api = HHApi()
    print("🌐 Сбор данных о компаниях и вакансиях...")

    for company_id in COMPANY_IDS:
        try:
            print(f" → Получение данных для компании ID: {company_id}")
            employer_data = api.get_employer(company_id)
            DatabaseManager.insert_employer(employer_data)

            vacancies = api.fetch_all_vacancies_for_employer(company_id)
            print(f"   → Найдено {len(vacancies)} вакансий.")

            for vac in vacancies:
                DatabaseManager.insert_vacancy(vac, company_id)

            time.sleep(0.5)  # чтобы не превысить лимиты API

        except Exception as e:
            print(f" ❌ Ошибка при обработке компании {company_id}: {e}")

    print("✅ Данные успешно загружены в БД.")

    # Шаг 3: Работа с DBManager
    db = DBManager()

    # Интерфейс взаимодействия с пользователем
    while True:
        print("\n" + "="*50)
        print("Выберите действие:")
        print("1. Показать компании и количество вакансий")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            data = db.get_companies_and_vacancies_count()
            print("\n--- Компании и количество вакансий ---")
            for company, count in data:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            data = db.get_all_vacancies()
            print("\n--- Все вакансии ---")
            for company, title, s_from, s_to, url in data:
                salary = f"от {s_from} до {s_to}" if s_from and s_to else "не указана"
                print(f"{company} | {title} | {salary} | {url}")

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"\nСредняя зарплата: {avg:.2f} руб.")

        elif choice == "4":
            data = db.get_vacancies_with_higher_salary()
            print(f"\n--- Вакансии с зарплатой выше средней ({db.get_avg_salary():.2f}) ---")
            for company, title, s_from, s_to, url in data:
                salary = f"от {s_from} до {s_to}" if s_from and s_to else "не указана"
                print(f"{company} | {title} | {salary} | {url}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ").strip()
            data = db.get_vacancies_with_keyword(keyword)
            print(f"\n--- Вакансии по запросу '{keyword}' ---")
            if data:
                for company, title, s_from, s_to, url in data:
                    salary = f"от {s_from} до {s_to}" if s_from and s_to else "не указана"
                    print(f"{company} | {title} | {salary} | {url}")
            else:
                print("Ничего не найдено.")

        elif choice == "0":
            print("👋 До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()