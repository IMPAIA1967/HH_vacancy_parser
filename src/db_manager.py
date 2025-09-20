import psycopg2

class DBManager:
    """Класс для управления базой данных вакансий."""

    def __init__(self, db_name, user, password, host, port):
        # Конструктор класса. Сохраняет параметры подключения как атрибуты объекта
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def _connect(self):
        """Внутренний метод для установления подключения к БД"""
        return psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        conn = self._connect()
        cur = conn.cursor()
        # SQL-запрос с JOIN и GROUP BY для подсчета вакансий
        query = """
            SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
            ORDER BY vacancy_count DESC
        """
        cur.execute(query)
        results = cur.fetchall()  # Получаем все строки результата
        cur.close()
        conn.close()
        return results  # Возвращаем список кортежей: [('Яндекс', 15), ('Сбер', 10)]

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием компании, названия, зарплаты и ссылки
        """
        conn = self._connect()
        cur = conn.cursor()
        query = """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            INNER JOIN employers e ON v.employer_id = e.employer_id
        """
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям (по полю salary_from).
        """
        conn = self._connect()
        cur = conn.cursor()
        # Функция AVG вычисляет среднее значение :cite[10]
        query = "SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL;"
        cur.execute(query)
        result = cur.fetchone()[0]  # fetchone() возвращает одну строку, [0] - первый элемент
        cur.close()
        conn.close()
        return round(result) if result else 0  # Округляем число

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней.
        Использует подзапрос
        """
        conn = self._connect()
        cur = conn.cursor()
        query = """
            SELECT * FROM vacancies
            WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL)
            ORDER BY salary_from DESC
        """
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых есть переданное слово.
        Использует оператор LIKE для поиска по шаблону :cite[4].
        """
        conn = self._connect()
        cur = conn.cursor()
        query = "SELECT * FROM vacancies WHERE title ILIKE %s"
        cur.execute(query, (f'%{keyword}%',))
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results