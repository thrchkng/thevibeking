class FieldIndexError(IndexError):
    def __str__(self):
        return 'Выведено значение за границами игрового поля'


class CellOccupiedError(Exception):
    def __str__(self):
        return 'Попытка исправить усугубила положение'
