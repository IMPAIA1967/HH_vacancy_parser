from api_hh import get_companies_and_vacancies

data = get_companies_and_vacancies()
print("Вот что в result:")
for item in data:
    print(f"{item['company_name']} — {len(item['vacancies'])} вакансий")