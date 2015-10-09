from django.db import connection
from django.core.management.base import BaseCommand
from django.core.management import call_command
from optparse import make_option


class Command(BaseCommand):
    __OPTION_NAME_DEFAULT_MAIL = 'email'
    __OPTION_NAME_DEFAULT_PW = 'password'
    __OPTION_NAME_NOSYNC = 'nosync'
    __OPTION_NAME_TRUNCATE = 'truncate'
    __OPTION_NAME_IGNORE_TABLES = 'ignoretables'

    help = 'Drops all database tables.'
    option_list = BaseCommand.option_list + (
        make_option('--' + __OPTION_NAME_DEFAULT_MAIL, action='store', help='Mail of user to create', default=None),
        make_option('--' + __OPTION_NAME_DEFAULT_PW, action='store', help='Password of user to create', default=None),
        make_option('--' + __OPTION_NAME_NOSYNC, action='store_true',
                    help='Option to skip calling migrate after resetdb', default=False),
        make_option('--' + __OPTION_NAME_TRUNCATE, action='store_true',
                    help='Option to truncate tables instead of drop them', default=False),
        make_option('--' + __OPTION_NAME_IGNORE_TABLES, action='store',
                    help='Option to pass a comma separated set of tables that should not be resetted', default=None))

    def handle(self, *args, **options):
        isTruncate = options[self.__OPTION_NAME_TRUNCATE]
        ignoreTables = options[self.__OPTION_NAME_IGNORE_TABLES].split(",") if options[self.__OPTION_NAME_IGNORE_TABLES] else []

        if isTruncate:
            ignoreTables.append('django_migrations')

        self.__dropOrTruncateTables(ignoreTables, isTruncate)

        if not options[self.__OPTION_NAME_NOSYNC]:
            call_command('migrate')

        if options[self.__OPTION_NAME_DEFAULT_MAIL] and options[self.__OPTION_NAME_DEFAULT_PW]:
            call_command('createtestuser', options[self.__OPTION_NAME_DEFAULT_MAIL], options[self.__OPTION_NAME_DEFAULT_PW],
                         superuser=True, staff=True, email=options[self.__OPTION_NAME_DEFAULT_MAIL])

    def __dropOrTruncateTables(self, ignoreTables, isTruncate):
        cursor = connection.cursor()
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        cursor.execute('START TRANSACTION; SET FOREIGN_KEY_CHECKS = 0')
        sqlCommand = "DROP TABLE IF EXISTS {}" if not isTruncate else "TRUNCATE {}"

        self.stdout.write('Dropping tables...')
        counter = 0
        for table in tables:
            if isTruncate and table[0] in ignoreTables:
                continue
            self.stdout.write('{} table {}'.format("Dropping" if not isTruncate else "Truncating", table[0]))
            cursor.execute(sqlCommand.format(table[0]))
            counter += 1

        cursor.execute('SET FOREIGN_KEY_CHECKS = 1; COMMIT')
        cursor.close()
        connection.close()

        self.stdout.write('\n{} {} tables'.format("Dropped" if not isTruncate else "Truncated", counter))
        if ignoreTables:
            self.stdout.write("Ignored {} tables: '{}'".format(len(ignoreTables), "','".join(ignoreTables)))
