"""A module for the data import handler"""
import pandas

class Data:
    def __init__(self, filename):
        self.filename = filename
        if filename.endswith('.xls') or filename.endswith('xlsx'):
            self.filetype = 'excel'
        elif filename.endswith('.csv'):
            self.filetype = 'csv'

    def read(self):
        if self.filetype == 'excel':
            self._read_excel()
        elif self.filetype == 'csv':
            self._read_csv()

    def _read_excel(self):
        self.df = pandas.read_excel(self.filename)

    def _read_csv(self):
        self.df = pandas.read_csv(self.filename)
        self.df.rename(columns=lambda x: x.strip(), inplace=True)

    def out(self):
        if self.df.ix[:, 0].dtype == object:
            df_dict = self.df.to_dict()
            name_column = self.df.columns[0]
            r = []
            for column in df_dict:
                if column != name_column:
                    d = {df_dict[name_column][indx]: int(df_dict[column][indx]) for
                            indx in df_dict[column]}
                    r.append(d)
        return r
