import datetime
from datetime import date

from connector import Connector
from engine_classes import HH, SuperJob


def cleaning_files(file_name):
    """Предварительно очищает содержимое файла"""
    with open(file_name, 'w'):
        pass


def formatting_all(name, url, description, city, publication_date, salary_from, salary_to, salary_currency) -> dict:
    """Возвращает отформатированный словарь, который приводит все данные к единому виду"""
    data_dict = {'title': name,
                 'url': url,
                 'description': description,
                 'city': city,
                 'publication_date': get_publication_date(publication_date),
                 'salary_from': salary_from,
                 'salary': get_salary(salary_from, salary_to, salary_currency)}
    return data_dict


def formatting_hh(job_title: str) -> list:
    """Возваращет приведенный к общему виду список данных, полученных из API для hh.ru"""
    hh = HH(job_title)
    vacancy_list = hh.get_request()
    vacancy_hh = []
    for i in vacancy_list:
        name = i['items'][0]['name']
        url = i['items'][0]['apply_alternate_url']
        description = i['items'][0]['snippet']['responsibility']
        city = i['items'][0]['area']['name']
        publication_date = i['items'][0]['published_at']
        salary_from = i['items'][0]['salary']['from'] if i['items'][0]['salary'] else None
        salary_to = i['items'][0]['salary']['to'] if i['items'][0]['salary'] else None
        salary_currency = i['items'][0]['salary']['currency'] if i['items'][0]['salary'] else None

        data_dict = formatting_all(name, url, description, city, publication_date, salary_from, salary_to, salary_currency)

        vacancy_hh.append(data_dict)

    return vacancy_hh


def formatting_sj(job_title: str) -> list:
    """Возваращет приведенный к общему виду список данных, полученных из API для hh.ru"""
    sj = SuperJob(job_title)
    vacancy_list = sj.get_request()
    vacancy_sj = []
    for i in vacancy_list:
        name = i['objects'][0]['profession']
        url = i['objects'][0]['link']
        description = i['objects'][0]['candidat']
        city = i['objects'][0]['town']['title']
        publication_date = i['objects'][0]['date_pub_to']
        salary_from = i['objects'][0]['payment_from'] if i['objects'][0]['payment_from'] != 0 else None
        salary_to = i['objects'][0]['payment_to'] if i['objects'][0]['payment_to'] != 0 else None
        salary_currency = i['objects'][0]['currency']
        data_dict = formatting_all(name, url, description, city, publication_date, salary_from, salary_to, salary_currency)
        vacancy_sj.append(data_dict)

    return vacancy_sj


def creating_a_list_with_all_vacancies(job_title: str) -> list:
    """Возвращает лист со всеми вакансиями по названию вакансии с superjob и hh.ru"""
    hh = formatting_hh(job_title)
    sj = formatting_sj(job_title)
    vacancy_list = []
    for hh_vacancy in hh:
        vacancy_list.append(hh_vacancy)

    for sj_vacancy in sj:
        vacancy_list.append(sj_vacancy)
    return vacancy_list


def writing_vacancies_to_a_file(file_name, data):
    """Запись данных в файл"""
    connector = Connector(file_name)
    connector.insert(data)


def get_salary(salary_from, salary_to, salary_currency) -> str:
    """Приводит зарплату к более читабельному виду"""
    if salary_from is not None and salary_to is not None:
        salary = f'от {int(salary_from * 77.02) if salary_currency == "USD" else salary_from}' \
                 f' до {int(salary_to * 77.02) if salary_currency == "USD" else salary_to} руб/мес '
    elif salary_from is None and salary_to is not None or salary_from == 0 and salary_to != 0:
        salary = f'Зарплата до {salary_to} руб/мес'
    elif salary_from is not None and salary_to is None or salary_from != 0 and salary_to == 0:
        salary = f'Зарплата от {salary_from} руб/мес'
    else:
        salary = 'Зарплата не указана'
    return salary


def get_publication_date(time: str | int) -> str:
    """Возвращает дату публикации"""
    if type(time) == str:
        index = time.index('T')
        publication_date = list(map(int, time[0:index].split('-')))
        the_date = date(publication_date[0], publication_date[1], publication_date[2])
        return the_date.strftime("%d.%m.%Y")
    elif type(time) == int:
        publication_date = datetime.datetime.fromtimestamp(time)
        return publication_date.strftime("%d.%m.%Y")
