import os
import sys
import csv
from django.db import connections, router
from django.contrib.humanize.templatetags.humanize import intcomma


class Copy(object):
    """
    Maps comma-delimited data file to a Django model
    and loads it into PostgreSQL databases using its
    COPY command.
    """
    def __init__(
        self,
        model,
        csv_path,
        mapping,
        using=None,
        delimiter=',',
        null=None
    ):
        self.model = model
        self.mapping = mapping
        if os.path.exists(csv_path):
            self.csv_path = csv_path
        else:
            raise ValueError("csv_path does not exist")
        if using is not None:
            self.using = using
        else:
            self.using = router.db_for_write(model)
        self.conn = connections[self.using]
        if self.conn.vendor != 'postgresql':
            raise TypeError("Only PostgreSQL backends supported")
        self.backend = self.conn.ops
        self.delimiter = delimiter
        self.null = null

        # Connect the headers from the CSV with the fields on the model
        self.header_field_crosswalk = []
        for h in self.get_headers():
            try:
                f_name = self.mapping[h]
            except KeyError:
                raise ValueError("Map does not include %s field" % h)
            try:
                f = [f for f in self.model._meta.fields if f.name == f_name][0]
            except IndexError:
                raise ValueError("Model does not include %s field" % f_name)
            self.header_field_crosswalk.append((h, f))

        self.temp_table_name = "temp_%s" % self.model._meta.db_table

    def save(self, silent=False, stream=sys.stdout):
        """
        Saves the contents of the CSV file to the database.

         silent:
           By default, non-fatal error notifications are printed to stdout,
           but this keyword may be set to disable these notifications.

         stream:
           Status information will be written to this file handle. Defaults to
           using `sys.stdout`, but any object with a `write` method is
           supported.
        """
        if not silent:
            stream.write("Loading CSV to %s\n" % self.model.__name__)

        # Connect to the database
        cursor = self.conn.cursor()

        # Create all of the raw SQL
        drop_sql = self.prep_drop()
        create_sql = self.prep_create()
        copy_sql = self.prep_copy()
        insert_sql = self.prep_insert()

        # Run all of the raw SQL
        cursor.execute(drop_sql)
        cursor.execute(create_sql)
        cursor.execute(copy_sql)
        cursor.execute(insert_sql)
        cursor.execute(drop_sql)

        if not silent:
            stream.write(
                "%s records loaded\n" % intcomma(self.model.objects.count())
            )

    def get_headers(self):
        """
        Returns the column headers from the csv as a list.
        """
        with open(self.csv_path, 'r') as infile:
            csv_reader = csv.reader(infile, delimiter=self.delimiter)
            headers = next(csv_reader)
        return headers

    def prep_drop(self):
        """
        Creates a DROP statement that gets rid of the temporary table.

        Return SQL that can be run.
        """
        return "DROP TABLE IF EXISTS %s;" % self.temp_table_name

    def prep_create(self):
        """
        Creates a CREATE statement that makes a new temporary table.

        Returns SQL that can be run.
        """
        sql = """CREATE TEMPORARY TABLE "%(table_name)s" (%(field_list)s);"""
        options = dict(
            table_name=self.temp_table_name,
        )
        field_list = []
        for header, field in self.header_field_crosswalk:
            string = '"%s" %s' % (header, field.db_type(self.conn))
            if hasattr(field, 'copy_type'):
                string = '"%s" %s' % (header, field.copy_type)
            field_list.append(string)
        options['field_list'] = ", ".join(field_list)
        return sql % options

    def prep_copy(self):
        """
        Creates a COPY statement that loads the CSV into a temporary table.

        Returns SQL that can be run.
        """
        sql = """
            COPY "%(db_table)s" (%(header_list)s)
            FROM '%(csv_path)s'
            WITH CSV HEADER %(extra_options)s;
        """
        options = {
            'db_table': self.temp_table_name,
            'csv_path': self.csv_path,
            'extra_options': '',
            'header_list': ", ".join([
                '"%s"' % h for h, f in self.header_field_crosswalk
            ])
        }
        if self.delimiter:
            options['extra_options'] += " DELIMITER '%s'" % self.delimiter
        if self.null:
            options['extra_options'] += " NULL '%s'" % self.null
        return sql % options

    def prep_insert(self):
        """
        Creates a INSERT statement that reorders and cleans up
        the fields from the temporary table for insertion into the
        Django model.

        Returns SQL that can be run.
        """
        sql = """
            INSERT INTO "%(model_table)s" (%(model_fields)s) (
            SELECT %(temp_fields)s
            FROM "%(temp_table)s");
        """
        options = dict(
            model_table=self.model._meta.db_table,
            temp_table=self.temp_table_name,
        )

        model_fields = []
        for header, field in self.header_field_crosswalk:
            if field.db_column:
                model_fields.append('"%s"' % field.db_column)
            else:
                model_fields.append('"%s"' % field.name)
        options['model_fields'] = ", ".join(model_fields)

        temp_fields = []
        for header, field in self.header_field_crosswalk:
            string = '"%s"' % header
            if hasattr(field, 'copy_template'):
                string = field.copy_template % dict(name=header)
            template_method = 'copy_%s_template' % field.name
            if hasattr(self.model, template_method):
                template = getattr(self.model(), template_method)()
                string = template % dict(name=header)
            temp_fields.append(string)
        options['temp_fields'] = ", ".join(temp_fields)
        return sql % options
