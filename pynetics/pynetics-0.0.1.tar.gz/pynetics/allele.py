import abc
import random


class Alleles(metaclass=abc.ABCMeta):
    # TODO TBD
    @abc.abstractmethod
    def get(self):
        # TODO TBD
        raise NotImplementedError()


class ListAlleles(Alleles):
    # TODO TBD
    def __init__(self, values):
        # TODO TBD
        self.__values = values

    def get(self):
        # TODO TBD
        return random.choice(self.__values)


class BinaryAlleles(ListAlleles):
    # TODO TBD
    def __init__(self):
        # TODO TBD
        super().__init__((0, 1))


class RangeAlleles(Alleles):
    # TODO TBD
    def __init__(self, a, b, integers=False):
        # TODO TBD
        self.__a = min(a, b)
        self.__b = max(a, b)
        self.__integers = integers

    def get(self):
        # TODO TBD
        return random.uniform(self.__a, self.__b) if not self.__integers else random.randint(self.__a, self.__b)
