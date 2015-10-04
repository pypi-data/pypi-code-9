# coding: utf-8
from m3.actions.results import PreJsonResult

from .encoder import JsonSerializableEncoder


class JsonSerializableResult(PreJsonResult):
    u""""Результат с сериализацией в JSON формат

    Отнаследован от PreJsonResult для совместимости
    """
    def __init__(self, data):
        super(JsonSerializableResult, self).__init__(data=data)
        self.encoder_clz = JsonSerializableEncoder
