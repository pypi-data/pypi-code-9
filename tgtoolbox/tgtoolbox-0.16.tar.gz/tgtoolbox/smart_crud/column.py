# -*- coding: utf-8 -*-
from markupsafe import Markup
from tg import request, url
from .field import Field
__author__ = 'vahid'


class Column(Field):

    def render_header(self):
        sorts = self.table.sorts.clone()
        sorts.add_or_toggle(self.label)

        url_params = dict(request.GET)
        url_params['sort_cols'] = unicode(sorts)
        url_ = url(request.path, url_params)

        sorts.remove(self.label)
        url_params['sort_cols'] = unicode(sorts)
        remove_url = url(request.path, url_params)

        if self.table.is_sortable(self):
            s = self.table.sorts.get(self.label)
            if s:
                icon = '<a href="%s"><i class="glyphicon glyphicon-remove"/></i></a>&nbsp;' % remove_url
                icon += '<a href="%(url)s"><i class="glyphicon glyphicon-arrow-%(icon_name)s"/></i></a>' % dict(
                    url=url_,
                    icon_name="down" if s.desc else "up"
                )
            else:
                icon = ''

            result = '%(icon)s<a href="%(url)s">%(title)s</a>' % \
                   dict(title=self.display_label,
                        icon=icon,
                        url=url_)
        else:
            result = self.display_label

        return Markup(result)