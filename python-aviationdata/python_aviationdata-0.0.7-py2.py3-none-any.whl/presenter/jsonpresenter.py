import json
from . import BasicPresenter


class JsonPresenter(BasicPresenter):
    def present(self):
        return json.dumps(self._data, sort_keys=True, indent=4, separators=(',', ': '))