from django.db import connection


class Query(object):
    def __init__(self, sql):
        self.sql = sql
        self._resultados = []

    def __getitem__(self, item):
        return self.resultado[item]

    def __nonzero__(self):
        return len(self._resultados) > 0

    @property
    def resultado(self):
        if self.tem_resultados:
            return self._resultados[0]
        return {}

    @property
    def resultados(self):
        if self.tem_resultados:
            return self._resultados
        return []

    def executar(self, *args):
        cursor = connection.cursor()
        cursor.execute(self.sql, args)
        desc = cursor.description

        if cursor.statusmessage.startswith("INSERT") \
                or cursor.statusmessage.startswith("UPDATE") \
                or cursor.statusmessage.startswith("DELETE"):
            return self

        self._resultados = [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

        return self

    @property
    def tem_resultados(self):
        return len(self._resultados) > 0