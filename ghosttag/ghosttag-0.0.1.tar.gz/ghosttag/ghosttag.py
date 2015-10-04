"""Tag editor for Ghost blogging platform

Usage:
    ghosttag.py list [--db-path=<path>]
    ghosttag.py update [--db-path=<path>] [--id=<tag-id>] [--name=<tag-name>] [--slug=<slug-name>]
    ghosttag.py delete  [--db-path=<path>] [--id=<tag-id>]
    ghosttag.py (-h | --help)
    ghosttag.py --version

Options:
  -h --help                 Show this screen.
  --version                 Show version.

"""
import sqlite3 as lite
import sys

from tabulate import tabulate
from docopt import docopt

tag_id_column = 0
tag_slug_column = 3
tag_name_column = 2
records = []


def setup_db(arguments):
    if arguments['--db-path']:
        try:
            conn = lite.connect(arguments['--db-path'])
            return conn
        except Exception as e:
            print 'Error. Can\'t connect to db.'
            print e
            sys.exit(0)
    else:
        db_url = raw_input("Where is the ghost-dev.db located?")
        if 'ghost-dev.db' not in db_url:
            print 'Make sure the path has ghost-dev.db'
            sys.exit(0)
        else:
            try:
                conn = lite.connect(db_url)
                return conn
            except Exception as e:
                print 'Error. Can\'t connect to db.'
                print e
                sys.exit(0)


def get_all_records(conn):
    with conn:
        conn.row_factory = lite.Row
        c = conn.cursor()
        c.execute('SELECT * FROM TAGS')
        for row in c.fetchall():
            records.append([row[tag_id_column], row[tag_name_column], row[tag_slug_column]])


def delete_record(conn, id_delete):
    try:
        c = conn.cursor()
        c.execute("DELETE FROM TAGS WHERE ID = ?", (id_delete,))
        conn.commit()

    except ValueError:
        print 'Invalid ID for deleting tag'


def update_name_or_slug(conn, id_update, name='', slug=''):
    try:
        c = conn.cursor()
        if name == '':
            c.execute("""UPDATE TAGS SET SLUG = ? WHERE ID = ?""", (slug, id_update))
        elif slug == '':
            c.execute("""UPDATE TAGS SET NAME = ? WHERE ID = ?""", (name, id_update))
        else:
            c.execute("""UPDATE TAGS SET SLUG = ?, NAME = ? WHERE ID = ?""", (slug, name, id_update))
        conn.commit()
        list_rows(conn)
    except lite.IntegrityError:
        print 'Cannot update tag with the same name'


def list_rows(conn):
    c = conn.cursor()
    c.execute('SELECT * FROM TAGS')
    headers = ['ID', 'Name', 'Slug']
    print tabulate(records, headers=headers)


def main():
    try:
        arguments = docopt(__doc__)
    except TypeError:
        print 'Error. Need arguments.'
        print __doc__
        sys.exit(0)

    conn = setup_db(arguments)
    get_all_records(conn)
    if arguments['list']:
        list_rows(conn)

    elif arguments['--id']:
        tag_id = arguments['--id']
        if arguments['update']:
            name = arguments['--name'] or ''
            slug = arguments['--slug'] or ''
            update_name_or_slug(conn, tag_id, str(name), str(slug))

        elif arguments['delete']:
            delete_record(conn, tag_id)
            list_rows(conn)

    else:
        print 'Error. Need id to delete.'
        print __doc__
        sys.exit(0)


if __name__ == '__main__':
    main()
