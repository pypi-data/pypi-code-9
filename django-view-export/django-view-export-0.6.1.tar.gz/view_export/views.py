import logging

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.utils import ProgrammingError
from django.http import Http404, HttpResponse

from .models import export_view, get_report_path

logger = logging.getLogger(__name__)

@user_passes_test(lambda u: u.is_staff)
def csv_view_export(request, view, prefix='v_'):
    """Export an SQL view as CSV for download.

    The purpose of the prefix is to restrict which relations are available for
    export. You probably don't want users to be able to export the auth_users
    table.

    Eventually you may end up with reports that are too large or complex to run
    within the web application's request/response cycle. TODO.

    Args:
        request: Django's Request object.
        view: The name of the SQL view to export. If the value provided
            doesn't include the prefix (eg. for vanity in URLs), the prefix will
            be added automatically. The name could also technically refer to a
            table if the table name included the prefix.
        prefix: The prefix you use on SQL relations to indicate they can be
            exported through this feature.

    """
    if not view.startswith(prefix):
        view = prefix + view
    filename = get_report_path(view[len(prefix):])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={filename}'.format(
            filename=filename)

    if view in getattr(settings, 'OFF_PEAK_VIEWS', []):
        try:
            with open(filename) as f:
                response.write(f.read())
        except IOError:
            logger.error(
                'User {user} tried to downloaded saved report {report} but it '
                'was not run overnight.'.format(
                    report=view, user=request.user))
            raise Http404('This saved report was not run overnight.')
        logger.info('User {user} downloaded saved report {report}'.format(
            report=view, user=request.user))
        return response

    try:
        export_view(view, response, prefix)
    except ProgrammingError as err:
        raise Http404(err)

    logger.info('User {user} downloaded live report {report}'.format(
        report=view, user=request.user))
    return response
