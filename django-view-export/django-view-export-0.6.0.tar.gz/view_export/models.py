import csv
import datetime
import os

from django.db import connection, models

def export_view(view_name, file, prefix):
    """Export an SQL view as CSV."""

    if not view_name.startswith(prefix):
        view_name = prefix + view_name
    cursor = connection.cursor()
    cursor.execute(
        'SELECT * FROM {view_name}'.format(
            view_name=connection.ops.quote_name(view_name)))

    writer = csv.writer(file)

    # Add field names from cursor metadata
    writer.writerow([title for title, *_ in cursor.description])

    for row in cursor:
        # Replace None with empty string
        writer.writerow(['' if i is None else i for i in row])


def get_report_path(slug, date=None):
    """Determine where to find/put a report based on its name.

    Args:
        slug: The report name minus the date and .csv extension. Avoid spaces
            for consistency.
        date: If you want a date other than today, specify it here.

    """
    if date is None:
        date = datetime.date.today()
    elif date == 'yesterday':
        date = datetime.date.today() - datetime.timedelta(days=1)
    return '{}-{:%Y-%m-%d}.csv'.format(slug, date)
