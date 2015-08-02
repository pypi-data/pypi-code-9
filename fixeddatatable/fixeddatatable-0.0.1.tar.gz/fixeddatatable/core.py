import json


class Column(object):
    """docstring for Column"""
    def __init__(self, label, key, width, num_format=None, sortable=False):
        self.label = label
        self.key = key
        self.width = width
        self.num_format = num_format

    def to_dict(self):
        columnData = {}
        if self.num_format is not None:
            columnData.update({'numFormat': self.num_format})
        # if self.url is not None:
        #     columnData.update({'url': self.url})
        return {
            'label': self.label,
            'dataKey': self.key,
            'width': self.width,
            'columnData': columnData
        }


class Table(object):

    def __init__(self, width, height, row_height, columns, rows,
                 filter=None):
        self.width = width
        self.height = height
        self.row_height = row_height
        self.columns = columns
        self.rows = rows
        self.filter = filter

    def json(self):
        table_params = {
            'width': self.width,
            'height': self.height,
            'rowHeight': self.row_height,
            'columnParams': [c.to_dict() for c in self.columns],
            'rows': self.rows,
            'filterControl': False
        }
        if self.filter is not None:
            table_params.update({
                'filterControl': True,
                'filterKey': self.filter['key'],
                'filterPlaceholder': self.filter.get('placeholder', '')
            })
        return json.dumps(table_params)
