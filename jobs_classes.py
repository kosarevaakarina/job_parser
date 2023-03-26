class Vacancy:
    __slots__ = ('title', 'url', 'description', 'salary')

    def __init__(self, title, url, description, salary):
        """Класс для репрезентативности выводимых данных"""
        self.title = title
        self.url = url
        self.description = description
        self.salary = salary

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"Vacancy(title='{self.title}', " \
               f"link='{self.url}', " \
               f"description='{self.description}', " \
               f"salary='{self.salary}')"

    def __gt__(self, other) -> bool:
        """Метод сравнения экземпляров класса (больше)"""
        return self.salary > other.salary

    def __lt__(self, other) -> bool:
        """Метод сравнения экземпляров класса (меньше)"""
        if other.salary is None:
            # e.g., 10 < None
            return False
        if self.salary is None:
            # e.g., None < 10
            return True

        return self.salary < other.salary


class CountMixin:
    def __init__(self):
        self.file_name = None
        self.count = 0

    @property
    def get_count_of_vacancy(self) -> int:
        """Возвращает количество вакансий от текущего сервиса."""
        return self.count

    @get_count_of_vacancy.setter
    def get_count_of_vacancy(self, file_name):
        """Получает количество вакансий из файла"""
        with open(file_name) as f:
            for line in f:
                if 'title' in line:
                    self.count += 1


class HHVacancy(Vacancy, CountMixin):  # add counter mixin
    """ HeadHunter Vacancy """

    def __str__(self) -> str:
        return f'HH: {self.title}, зарплата: {self.salary} руб/мес'


class SJVacancy(Vacancy, CountMixin):  # add counter mixin
    """ SuperJob Vacancy """

    def __str__(self) -> str:
        return f'SJ: {self.title}, зарплата: {self.salary} руб/мес'


def sorting_city(vacancies: list, city: str) -> list:
    """Сортировка вакансий по названию города"""
    sorted_by_city = []
    for i in vacancies:
        if city in i['city']:
            sorted_by_city.append(i)
    return sorted_by_city


def sorting(vacancies: list, key_search: str) -> list:
    """Сортирует список вакансий по зарплате, где key_search может быть любым параметром"""
    sorted_by_key_search = sorted(vacancies, key=lambda x: x.get(key_search), reverse=True)
    return sorted_by_key_search


def get_top(vacancies: list, top_count: int):
    """ Возвращает ТОП записей из вакансий по зарплате"""
    try:
        for i in range(top_count):
            title = vacancies[i]['title']
            url = vacancies[i]['url']
            description = vacancies[i]['description']
            salary = vacancies[i]['salary']
            if 'hh.ru' in url:
                print(HHVacancy(title, url, description, salary))
            else:
                print(SJVacancy(title, url, description, salary))

    except IndexError:
        print(f'Нет {top_count} записей вакансий')
