from connector import Connector
from utils import creating_a_list_with_all_vacancies, writing_vacancies_to_a_file, cleaning_files
from jobs_classes import sorting_city, sorting, get_top


try:
    # предварительная очистка создаваемого файла для обновления данных
    cleaning_files('sorted_vacancies.json')
    # получение названия должности для дальнейшего поиска
    job_title = input("Введите название интересующей профессии: ").strip()
    # получение листа со всеми вакансиями по данному запросу
    vacancy_list = creating_a_list_with_all_vacancies(job_title)

    try:
        """Сортировка по названию города"""
        # получение названия города для дальнейшего поиска
        user_input_city = input("Введите город для поиска: ").strip().title()
        # получение листа с вакансиями в конкретном городе
        sorted_by_city = sorting_city(vacancy_list, user_input_city)

        try:
            # выводит необходимое количество вакансий
            user_input_count_vacancy = int(input("Введите количество вакансий: "))

            new_content = []
            for i in vacancy_list:
                if i['salary_from'] is not None:
                    new_content.append(i)

            """Сортировка по зарплате"""

            # сортировка вакансий по зп
            sorted_by_salary = sorting(new_content, 'salary_from')
            # запись отсортированных вакансий в файл для вывода более подробной информации, если необходимо
            writing_vacancies_to_a_file('sorted_vacancies.json', sorted_by_salary)

            """Сортировка по дате публикации"""

            try:
                vacancies_by_date = input("Хотите ли вывести вакансии за определенную дату? (да/нет)").strip().lower()
                if vacancies_by_date == 'да' or vacancies_by_date == 'yes':
                    user_input_data = input("За какую дату вывести вакансии: ")
                    c = Connector('sorted_vacancies.json')
                    sorted_by_date = c.select({'publication_date': user_input_data})
                    get_top(sorted_by_salary, user_input_count_vacancy)
                else:
                    sorted_by_date = input("Сортировать по дате публикации? (да/нет").strip().lower()
                    if sorted_by_date == 'да' or sorted_by_date == 'yes':
                        list_sorted_by_date = sorting(sorted_by_salary, "publication_date")
                        get_top(list_sorted_by_date, user_input_count_vacancy)
                    else:
                        get_top(sorted_by_salary, user_input_count_vacancy)
            except AttributeError:
                print("Вакансий в эту дату нет, или дата указано не корректно. Начните сначала")
        except ValueError:
            print("Количество вакансий указано не корректно. Начните сначала")

    except AttributeError:
        print(f"Вакансий в этом городе нет. Начните сначала")

except AttributeError:
    print("Такой вакансии нет, попробуйте указать вакансию корректно")
