import datetime
import logging
import os

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.http import Http404, HttpResponse
# If on Python 3, Pandas can use the built-in UnicodeWriter. Otherwise it will
# fall back to an Python 2.7 compatible version.
from pandas.core.common import UnicodeWriter

from .models import config

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff)
def csv_view_export(request, view):
    """Export a view as CSV.

    View name may be supplied with or without the "v_" prefix as it will be
    added if necessary.

    """
    if not view.startswith('v_'):
        view = 'v_' + view
    response = HttpResponse(content_type='text/csv')
    filename = "{view_name}-{now:%Y-%m-%d}.csv".format(
            view_name=view[2:], now=datetime.datetime.now())
    response['Content-Disposition'] = "attachment; filename={filename}".format(
            filename=filename)

    if view in config['OFF_PEAK_VIEWS']:
        file_path = os.path.join(settings.REPORT_DIR, filename)
        try:
            f = open(file_path, 'rb')
        except IOError:
            logger.error(
                "User {user} tried to downloaded saved report {report} but it "
                "wasn't run last night.".format(
                    report=view, user=request.user))
            return HttpResponse(
                "This saved report was not run last night.",
                status=404)
        else:
            response.write(f.read())
            logger.info("User {user} downloaded saved report {report}".format(
                report=view, user=request.user))
            return response

    writer = UnicodeWriter(response, encoding='utf-8')
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT * FROM {view_name}'.format(
            view_name=connection.ops.quote_name(view)))
    except: # where's a ProgrammingError defined?
        raise Http404
    # Add field names from cursor metadata
    writer.writerow([i[0] for i in cursor.description])
    for row in cursor:
        # Replace None with empty string
        row = [i if i is not None else '' for i in row]

        writer.writerow(row)
    logger.info("User {user} downloaded live report {report}".format(
        report=view, user=request.user))
    return response
