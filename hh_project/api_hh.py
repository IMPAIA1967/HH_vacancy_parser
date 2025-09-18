from unittest import result

import requests


COMPANIES = [
    "Яндекс",
    "Сбер",
    "Тинькофф",
    "ВК",
    "Озон",
    "Авито",
    "МТС",
    "Ростелеком",
    "Лаборатория Касперского",
    "МегаФон"
]

def get_companies_id(companies_name: str, company_name=None) -> int or None:
    """Получаем ID компании по названию"""
    url = "https://api.hh.ru/employers"
    params = {"text": company_name, "per_page": 1}
    response = requests.get(url, params=params)
    data = response.json()
    if data["items"]:
        return data["items"][0]["id"]
    return None


def get_vacancies_by_employer(employer_id: int):
    """Получаем вакансии компании по ID"""
    url = f"https://api.hh.ru/employers"
    params = {"employer_id": employer_id, "per_page": 10}
    response = requests.get(url, params=params)
    return response.json()["items"]


def get_companies_and_vacancies(company_name=None):
    """Проходим по всем 10 компаниям, находим их ID,
     потом вакансии, и сохраняем всё в список"""
    results = []
    for company in COMPANIES:
        print(f"Ищем компанию: {company_name}")
        employer_id = get_companies_id(company_name)
        if employer_id:
            vacancies = get_vacancies_by_employer(employer_id)
            result.append({
                "company_name": company_name,
                "employer_id": employer_id,
                "vacancies": vacancies
            })
        else:
            print(f"Компания '{company_name}' не найдена")
    return results