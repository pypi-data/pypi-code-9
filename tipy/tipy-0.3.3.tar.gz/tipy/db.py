#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Classes to connect to databases."""

from sqlite3 import connect, OperationalError
from re import compile
from tipy.lg import lg


class OpenFileError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr('Cannot open file "%s".' % self.value)


class DatabaseConnector(object):
    """Implement methods for accessing the databases.

    G{classtree DatabaseConnector}
    """

    singleQuoteRegex = compile("'")

    def __init__(self, dbname, maxN=1):
        """DababaseConnector creator.

        @param dbname:
            Path to the database file.
        @type dbname: str
        @param maxN:
            The n in the longer database n-grams table.
        @type maxN: int
        """
        self.maxN = maxN
        self.dbname = dbname

    def crt_ngram_table(self, n=1):
        """Creates a table in the database to store n-gram of a given n.

        @param n:
            The n in n-gram. A table called [n]_gram (where [n] is the n
            parameter) will be created.
        @type n: int
        """
        query = 'CREATE TABLE IF NOT EXISTS _{0}_gram ('.format(n)
        unique = ''
        for i in reversed(range(n)):
            if i != 0:
                unique += 'word_{0}, '.format(i)
                query += 'word_{0} TEXT, '.format(i)
            else:
                unique += 'word'
                query += 'word TEXT, count INTEGER, UNIQUE({0}) );'.format(
                    unique)
        self.execute_sql(query)

    def drop_ngram_table(self, n=1):
        """Drop a n-gram table in the database.

        @param n:
            The n in n-gram.
        @type n: int
        """
        query = 'DROP TABLE IF EXISTS _{0}_gram;'.format(n)
        self.execute_sql(query)

    def crt_index(self, n):
        """Create the index for the table storing n-gram of given n.

        @param n:
            The n in n-gram.
        @type n: int
        """
        for i in reversed(range(n)):
            if i != 0:
                query = 'CREATE INDEX IF NOT EXISTS idx_{0}_gram_{1} ON '\
                        '_{0}_gram(word_{1});'.format(n, i)
                self.execute_sql(query)

    def dlt_index(self, n):
        """Drop the index for the table storing n-gram of given n.

        @param n:
            The n in n-gram.
        @type n: int
        """
        for i in reversed(range(n)):
            if i != 0:
                query = 'DROP INDEX IF EXISTS idx_{0}_gram_{1};'.format(
                    n, i)
                self.execute_sql(query)

    def create_table_if_not_exists(self):
        """Create the database tables and indexes if they don't exists.

        This is usefull to avoid crash when trying to hit an unexisting table.
        """
        for n in range(1, int(self.maxN) + 1):
            self.crt_ngram_table(n)
            self.crt_index(n)

    def ngrams(self, withCounts=False):
        """Returns all ngrams that are in every tables of the database.

        @note: The result is convert to tuple before being returned because it
               is used as a dictionary key and only immutable types can be used
               as dictionary key, so list cannot.

        @param withCounts:
            Indicate if the ngrams counts (number of occurences) should be
            returned too.
        @type withCounts: bool

        @return:
            The n-grams of each tables of the database.
        @rtype: tuple
        """
        query = 'SELECT '
        for i in reversed(range(self.maxN)):
            if i != 0:
                query += 'word_{0}, '.format(i)
            elif i == 0:
                query += 'word'
        if withCounts:
            query += ', count'
        query += ' FROM _{0}_gram;'.format(self.maxN)
        result = self.execute_sql(query)
        for row in result:
            yield tuple(row)

    def sum_ngrams_occ(self, n):
        """Compute the occurences sum of every n-grams of given n in database.

        @param n:
            The n in n-gram.
        @type n: int

        @return:
            The sum of the number of occurences of every n-grams in the n-grams
            table of given n in the database.
        @rtype: int
        """
        query = 'SELECT SUM(count) from _' + str(n) + '_gram;'
        return self.extract_first_integer(self.execute_sql(query))

    def ngrams_in_table(self, n):
        """Compute the number of n-grams in the n-grams table of given n.

        @param n:
            The n in n-gram.
        @type n: int

        @return:
            The number of n-grams in the n-grams table of given n in the
            database.
        @rtype: int
        """
        table = '_' + str(n) + '_gram'
        query = 'SELECT Count() from _' + str(n) + '_gram;'
        return self.extract_first_integer(self.execute_sql(query))

    def ngram_count(self, ngram):
        """Retrieve the number of occurences of a given ngram in the database.

        @param ngram:
            The n-gram for which number of occurences must be retrieved.
        @type ngram: list

        @return:
            The number of occurences of the n-gram or 0 if the n-gram is not
            in the databade.
        @rtype: int
        """
        query = 'SELECT count FROM _{0}_gram'.format(len(ngram))
        query += self.make_where_clause(ngram) + ';'
        return self.extract_first_integer(self.execute_sql(query))

    def ngram_table_tp(self, ngram, limit=-1):
        """Retrieve the n-gram records which complete the given n-gram.

        For instance, if ngram is::
            ['on', 'the', 'ta']
        Then the returned records would be somthing like::
            [['on', 'the', 'table'  ], 5]
            [['on', 'the', 'take'   ], 1]
            [['on', 'the', 'taskbar'], 1]

        @note: the query makes sure the n-grams are returned in descending order
               according to their number of occurences. This is important
               because the predictors predict() methods which would call this
               method can limit their suggestion number so the most probable
               suggestions (which are based on most frequent n-grams) must be
               append to the list first.

        @param ngram:
            The n-gram words of the record to retrieve in the database.
        @type ngram: list
        @param limit:
            Maximum number of records to retrieve.
        @type limit: int

        @return:
            Return the n-grams records (n-gram words + number of occurences)
            completing the n-gram in the database or an empty list if no n-grams
            have been found.
        @rtype: list
        """
        query = '{0} FROM _{1}_gram {2} ORDER BY count DESC'.format(
            self.make_select_like_clause(len(ngram)), len(ngram),
            self.make_where_like_clause(ngram))
        if limit < 0:
            query += ';'
        else:
            query += ' LIMIT ' + str(limit) + ';'
        return self.execute_sql(query)

    def insert_ngram(self, ngram, count):
        """Insert an n-gram with its number of occurences into the database.

        @param ngram:
            The n-gram to insert.
        @type ngram: list
        @param count:
            The number of occurences of the n-gram to insert. It is usually 1 as
            the n-grams should be inserted in the database only if they are not
            already in it and they are added when they are read on the input
            buffer.
        @type count: int
        """
        query = 'INSERT INTO _{0}_gram {1};'.format(len(ngram),
                self.make_values_clause(ngram, count))
        self.execute_sql(query)

    def update_ngram(self, ngram, count):
        """Update an n-gram number of occurences in the database.

        @warning: The ngram has to be in the database, otherwise this method
            will fail.

        @param ngram:
            The n-gram to update (!!! should be in the database !!!).
        @type ngram: list
        @param count:
            The number of occurences of the n-gram.
        @type count: int
        """
        query = 'UPDATE _{0}_gram SET count = {1}'.format(len(ngram), count)
        query += self.make_where_clause(ngram) + ';'
        self.execute_sql(query)

    def remove_ngram(self, ngram):
        """Remove a given ngram from the databae.

        @warning: The ngram has to be in the database, otherwise this method
            will fail.

        @param ngram:
            The n-gram to delete (!!! should be in the database !!!).
        @type ngram: list
        """
        query = 'DELETE FROM _{0}_gram'.format(len(ngram))
        query += self.make_where_clause(ngram) + ';'
        self.execute_sql(query)

    def make_values_clause(self, ngram, count):
        ng = [self.singleQuoteRegex.sub("''", n) for n in ngram]
        valuesClause = "VALUES('" + "', '".join(ng) + "', {0})".format(count)
        return valuesClause

    def make_where_clause(self, ngram):
        whereClause = " WHERE"
        for i in range(len(ngram)):
            n = self.singleQuoteRegex.sub("''", ngram[i])
            if i < (len(ngram) - 1):
                whereClause += " word_{0} = '{1}' AND".format(
                    len(ngram) - i - 1, n)
            else:
                whereClause += " word = '{0}'".format(n)
        return whereClause

    def make_select_like_clause(self, n):
        result = "SELECT "
        for i in reversed(range(1, n)):
            result += "word_{0}, ". format(i)
        result += "word, count"
        return result

    def make_where_like_clause(self, ngram):
        whereClause = " WHERE"
        for i in range(len(ngram)):
            if i < (len(ngram) - 1):
                whereClause += " word_{0} = '{1}' AND".format(
                    len(ngram) - i - 1, ngram[i])
            else:
                whereClause += " word LIKE '{0}%'".format(ngram[-1])
        return whereClause

    def extract_first_integer(self, table):
        count = 0
        if table and table[0] and table[0][0]:
            count = int(table[0][0])
        if not count > 0:
            count = 0
        return count


class SqliteDatabaseConnector(DatabaseConnector):
    """Database connector for sqlite databases.

    G{classtree SqliteDatabaseConnector}
    """

    def __init__(self, dbname, maxN=1):
        """SqliteDatabaseConnector creator.

        @param dbname:
            Path to the database file.
        @type dbname: str
        @param maxN:
            The n in the longer database n-grams table.
        @type maxN: int
        """
        DatabaseConnector.__init__(self, dbname, maxN)
        self.con = None
        self.open_database()
        self.create_table_if_not_exists()

    def commit(self):
        """Send a commit to the database."""
        self.con.commit()

    def open_database(self):
        """Open the database."""
        try:
            self.con = connect(self.dbname)
        except OperationalError:
            lg.error("Cannot open database file '%s'" % (self.dbname))
            raise OpenFileError(self.dbname)

    def close_database(self):
        """Close the database."""
        if self.con:
            self.con.close()

    def execute_sql(self, query):
        """Execute a query string on an open database.

        @param query:
            The query to execute.
        @type query: str

        @return:
            The query result.
        @rtype: list
        """
        c = self.con.cursor()
        c.execute(query)
        result = c.fetchall()
        return result


def insert_ngrams(ngramMap, n, outfile, append=False, createIndex=False,
                  callback=None):
    """Insert every n-grams of the map in the database.

    This function open a database and insert or update every n-grams of the
    given list in it.

    @param ngramMap:
        The list of n-grams to insert or update.
    @type ngramMap: list
    @param n:
        The n in n-gram.
    @type n: int
    @param outfile:
        Path to the database.
    @type outfile: str
    @param append:
        Indicate weither the n-gram should be append to the database. If the
        database isn't empty, this function could raise conflict when trying
        to insert an n-gram which is already in the database. When such
        conflicts happen the append value is important:
            - True: conflicting records count values are updated.
            - False: conflicting records are replaced by new records.
    @type append: bool
    @param createIndex:
        Indicate weither the database table indexes should be created.
    @type createIndex: bool
    @param callback:
        The callback is used to show the progress percentage. In the gui a
        callback method is implemented to update a progress bar showing the
        n-grams insertion progress (cf. py).
    @type callback: fun(float, ...)
    """
    progress = 0
    sql = SqliteDatabaseConnector(outfile, n)
    sql.crt_ngram_table(n)
    for ngram, count in ngramMap.items():
        if append:
            oldCount = sql.ngram_count(ngram)
            if oldCount > 0:
                sql.update_ngram(ngram, oldCount + count)
            else:
                sql.insert_ngram(ngram, count)
        else:
            sql.remove_ngram(ngram)     # avoid IntegrityError
            sql.insert_ngram(ngram, count)
        progress += 100 / len(ngramMap)
        if callback:
            callback(progress)
    sql.commit()
    if createIndex and not append:
        sql.crt_index(n)
    sql.close_database()
