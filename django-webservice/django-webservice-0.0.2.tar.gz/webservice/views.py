from datetime import datetime
from email.utils import parsedate as http_parse_date

import pytz
from django.http.response import HttpResponseNotModified
from django.db.models import Q

from webservice import models


def delta_update(cls):
    original_list = getattr(cls, 'list', None)

    def decorator_list(self, request, *args, **kwargs):
        last_modified_header = request.META.get("HTTP_IF_MODIFIED_SINCE")
        if last_modified_header is not None:
            parsed_modified = datetime(*http_parse_date(last_modified_header)[:6])
            modified_since = pytz.UTC.localize(parsed_modified)
            modified_since_qs = cls.queryset.filter(Q(updated__gte=modified_since) &
                                                    (Q(status=models.SynchronizedModel.STATUS_PUBLISHED)
                                                     | Q(status=models.SynchronizedModel.STATUS_PUBLISHED_DRAFT)
                                                     | Q(status=models.SynchronizedModel.STATUS_PUBLISHED_DELETED)))
            if modified_since_qs.count() == 0:
                return HttpResponseNotModified()
            else:
                self.queryset = modified_since_qs
        else:
            self.queryset = self.queryset.filter(status=models.SynchronizedModel.STATUS_PUBLISHED)
        return original_list(self, request, *args, **kwargs)

    cls.list = decorator_list

    return cls