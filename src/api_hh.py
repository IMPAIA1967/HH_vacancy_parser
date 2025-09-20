import requests  # для выполнения HTTP-запросов


def get_employer_data(employer_id):
    """
    Эта функция получает данные о компании по ее ID на HH.ru
    """
    # Формируем URL для запроса к API HH.ru для получения данных о конкретном работодателе
    url = f"https://api.hh.ru/employers/{employer_id}"

    # Делаем GET-запрос к API. Параметры нужны, чтобы немного фильтровать вакансии
    response = requests.get(url, params={'per_page': 10, 'only_with_vacancies': True})

    # Проверяем, что запрос успешен
    data = response.json()  # Преобразуем ответ от сервера в удобный формат Python (словарь)


    employer_data = {
        'id': data['id'],  # ID компании
        'name': data['name'],  # Название компании
        'url': data['alternate_url']  # Ссылка на страницу компании на HH
    }
    return employer_data


def get_vacancies_data(employer_id):
    """
    Эта функция получает список вакансий для конкретной компании.
    """
    url = f"https://api.hh.ru/vacancies?employer_id={employer_id}"
    response = requests.get(url, params={'per_page': 100})  # per_page - сколько вакансий просим
    data = response.json()

    vacancies_list = []  # Создаем пустой список, куда будем складывать данные о вакансиях
    for item in data['items']:  # Проходим по каждой вакансии в ответе
        # Проверяем, указана ли зарплата. Если нет, ставим None
        salary = item['salary']
        if salary is not None:
            # Зарплата может указываться "от", "до" или в виде вилки. Берем нижнюю границу.
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            # Если указана и "от", и "до", можно посчитать среднее, но мы возьмем from
        else:
            salary_from = None
            salary_to = None

        # Формируем словарь с данными о вакансии
        vacancy_info = {
            'id': item['id'],
            'employer_id': employer_id,  # Важно! Это связь с таблицей компаний
            'name': item['name'],
            'salary_from': salary_from,
            'salary_to': salary_to,
            'url': item['alternate_url'],
            'description': item['snippet']['requirement']  # Небольшое описание
        }
        vacancies_list.append(vacancy_info)  # Добавляем вакансию в общий список
    return vacancies_list