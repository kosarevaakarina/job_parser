import json
import os.path


class Connector:
    """
    Класс коннектор к файлу, обязательно файл должен быть в json формате
    не забывать проверять целостность данных, что файл с данными не подвергся
    внешнего деградации
    """
    __data_file = None

    def __init__(self, data_file):
        self.__data_file = data_file

    @property
    def data_file(self):
        return self.__data_file

    @data_file.setter
    def data_file(self, value):
        self.__data_file = value
        self.__connect()

    def __connect(self):
        """
        Проверка на существование файла с данными и
        создание его при необходимости
        Также проверить на деградацию и возбудить исключение
        если файл потерял актуальность в структуре данных
        """
        if not os.path.exists(self.__data_file):
            with open(self.__data_file, 'w') as file:
                file.write(json.dumps([]))

    def insert(self, data_vacancy: list):
        """
        Запись данных в файл с сохранением структуры и исходных данных
        """
        with open(self.__data_file, 'a', encoding="UTF-8") as file:
            json_data = json.dumps(data_vacancy, ensure_ascii=False, indent=2)
            file.write(json_data)

    def select(self, query: dict) -> list:
        """
        Выбор данных из файла с применением фильтрации
        query содержит словарь, в котором ключ это поле для
        фильтрации, а значение это искомое значение, например:
        {'price': 1000}, должно отфильтровать данные по полю price
        и вернуть все строки, в которых цена 1000
        """
        try:
            with open(self.__data_file, 'r', encoding='utf-8') as f:
                available_data = json.load(f)

            results = []
            for i in available_data:
                if all(i.get(key) == value for key, value in query.items()):
                    results.append(i)
            return results
        except Exception:
            print("Фильтрация недопустима")

    def delete(self, query: dict):
        """
        Удаление записей из файла, которые соответствуют запрос,
        как в методе select. Если в query передан пустой словарь, то
        функция удаления не сработает
        """
        if not len(query):
            return
        with open(self.__data_file, 'r', encoding='utf-8') as f:
            available_data = json.load(f)
        with open(self.__data_file, 'w', encoding='utf-8') as f:
            available_data = list(
                filter(lambda item: not all(item[key] == value for key, value in query.items()), available_data))
            json.dump(available_data, f, indent=2, ensure_ascii=False)
