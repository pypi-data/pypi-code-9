# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import io
import textwrap

import jinja2

from fabric.api import put, sudo, settings
from fabric.contrib.files import upload_template


POSTGRES_TEMPLATE = \
"""#!/bin/sh
# Backup all postgres databases to Amazon S3

S3_BUCKET_NAME='{{S3_BUCKET_NAME}}'
PGP_KEY_ID='{{PGP_KEY_ID}}'
cd /tmp
for DB in $(su postgres -c "psql -c 'SELECT datname FROM pg_database WHERE datistemplate = false' -t")
do
    TMPFILE=$(mktemp)
    DUMPFILE="postgres-dump--$DB@$(hostname)::$(date --rfc-3339=ns | sed 's/ /T/g')"
    su postgres -c "pg_dump $DB" | gpg --batch --trust-model direct -e -r "$PGP_KEY_ID" > "$TMPFILE"
    s3cmd put "$TMPFILE" "s3://$S3_BUCKET_NAME/{% if S3_PREFIX %}{{S3_PREFIX}}/{% endif %}$DUMPFILE"
    rm "$TMPFILE"
done
"""

MYSQL_TEMPLATE = \
"""#!/bin/sh
CONFIGDIR='{{DB_CONFIG_DIR}}'
S3_BUCKET_NAME='{{S3_BUCKET_NAME}}'
PGP_KEY_ID='{{PGP_KEY_ID}}'

for DB in "$DB_CONFIG_DIR"/*.my
do
	source "$DB"
	TMPFILE=$(mktemp)
	DUMPFILE="mysql-dump--$DBNAME@$(hostname)::$(date --rfc-3339=ns | sed 's/ /T/g')"
	mysqldump --user="$DBUSER" --password="$DBPASS" --databases "$DBNAME" | gpg --batch --trust-model direct -e -r "$PGP_KEY_ID" > "$TMPFILE"
	s3cmd put "$TMPFILE" "s3://$S3_BUCKET_NAME/{% if S3_PREFIX %}{{S3_PREFIX}}/{% endif %}$DUMPFILE"
	rm "$TMPFILE"
done
"""

DIRECTORY_SYNC_TEMPLATE = \
"""#!/bin/sh

s3cmd sync '{{DIRECTORY}}' s3://{{S3_BUCKET_NAME}}/{% if S3_PREFIX %}{{S3_PREFIX}}/{% endif %}

"""

def s3_mysql_backup(databases=None, s3_bucketname=None, pgp_encrypt_to=None,
                    db_configfiles_dir='/etc/db_backups_private', s3_prefix=None):
    """
    Generate cron script that will backup MySQL databases listed in ``databases``.
    ``databases`` should be a list of dictionary-like objects with the following mandatory keys:
        ``username``
        ``password``
        ``db_name``
    Dumping of remote databases is not supported.
    """
    if not all(databases, s3_bucketname, pgp_encrypt_to):
         raise TypeError("missing required arguments")

    sudo("mkdir -m 0700 -p '%s'" % db_configfiles_dir)
    with settings(sudo_user='root'):
        for database in databases:
            put(
                io.StringIO(jinja2.Template(textwrap.dedent(
                    """
                    DBPASS='{{password}}'
                    DBUSER='{{username}}'
                    DBNAME='{{db_name}}
                    """
                )).render(database)),
                remote_path='%s/%s.my' % (db_configfiles_dir, database['db_name']),
                use_sudo=True,
                mode=0400,
            )

    return jinja.Template(MYSQL_TEMPLATE).render({
        'DB_CONFIG_DIR': db_configfiles_dir,
        'S3_BUCKET_NAME': s3_bucketname,
        'PGP_KEY_ID': pgp_encrypt_to,
        'S3_PREFIX': s3_prefix
    })


def install_s3_postgres_backup(databases=None, s3_bucketname=None, pgp_encrypt_to=None, s3_prefix=None):
    """
    Backup all postgres databases individually and sync to the given s3 bucket.
    Database dumps will be encrypted with gpg using the given public key id (64bits).
    This function assumes the running user has a valid s3cmd config in their home directory.
    """
    if not pgp_encrypt_to or not s3_bucketname:
        raise TypeError("missing required arguments")

    return jinja2.Template(POSTGRES_TEMPLATE).render({
        'S3_BUCKET_NAME': s3_bucketname,
        'PGP_KEY_ID': pgp_encrypt_to,
        'S3_PREFIX': s3_prefix,
    })


def s3_directory_sync(directory=None, s3_bucketname=None, s3_prefix=None):
    if not directory or not s3_bucketname:
        raise TypeError("missing required arguments")

    return jinja2.Template(DIRECTORY_SYNC_TEMPLATE).render({
        'DIRECTORY': directory,
        'S3_BUCKET_NAME': s3_bucketname,
        'S3_PREFIX': s3_prefix,
    })
