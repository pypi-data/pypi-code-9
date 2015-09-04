class BasicPresenter(object):
    _data = None

    def __init__(self, data):
        self._data = data

    def present(self):
        raise NotImplementedError()

    def __str__(self):
        return self.present()

from jsonpresenter import JsonPresenter
from humanpresenter import HumanPresenter