# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2015 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Views for Email Bounces
"""

from __future__ import unicode_literals

import os
import datetime

from rattail.db import model
from rattail.bouncer import get_handler
from rattail.bouncer.config import get_profile_keys

import formalchemy
from pyramid.response import FileResponse
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from webhelpers.html import literal

from tailbone.db import Session
from tailbone.views import SearchableAlchemyGridView, CrudView
from tailbone.forms import renderers
from tailbone.forms.renderers.bouncer import BounceMessageFieldRenderer
from tailbone.grids.search import BooleanSearchFilter, ChoiceSearchFilter


class EmailBouncesGrid(SearchableAlchemyGridView):
    """
    Main grid view for email bounces.
    """
    mapped_class = model.EmailBounce
    config_prefix = 'emailbounces'

    def __init__(self, request):
        super(EmailBouncesGrid, self).__init__(request)
        self.handler_options = [('', '(any)')] + sorted(get_profile_keys(self.rattail_config))

    def join_map(self):
        return {
            'processed_by': lambda q: q.outerjoin(model.User),
        }

    def filter_map(self):

        def processed_is(q, v):
            if v == 'True':
                return q.filter(model.EmailBounce.processed != None)
            else:
                return q.filter(model.EmailBounce.processed == None)

        def processed_nt(q, v):
            if v == 'True':
                return q.filter(model.EmailBounce.processed == None)
            else:
                return q.filter(model.EmailBounce.processed != None)

        return self.make_filter_map(
            exact=['config_key'],
            ilike=['bounce_recipient_address', 'intended_recipient_address'],
            processed={'is': processed_is, 'nt': processed_nt},
            processed_by=self.filter_ilike(model.User.username))

    def filter_config(self):
        return self.make_filter_config(
            include_filter_config_key=True,
            filter_type_config_key='is',
            filter_label_config_key="Source",
            filter_factory_config_key=ChoiceSearchFilter(self.handler_options),
            filter_factory_processed=BooleanSearchFilter,
            filter_type_processed='is',
            processed=False,
            include_filter_processed=True,
            filter_label_bounce_recipient_address="Bounced To",
            filter_label_intended_recipient_address="Intended For")

    def sort_config(self):
        return self.make_sort_config(sort='bounced', dir='desc')

    def sort_map(self):
        return self.make_sort_map(
            'config_key', 'bounced', 'bounce_recipient_address', 'intended_recipient_address',
            processed_by=self.sorter(model.User.username))

    def grid(self):
        g = self.make_grid()
        g.bounced.set(renderer=renderers.DateTimeFieldRenderer(self.rattail_config))
        g.configure(
            include=[
                g.config_key.label("Source"),
                g.bounced,
                g.bounce_recipient_address.label("Bounced To"),
                g.intended_recipient_address.label("Intended For"),
                g.processed_by,
                ],
            readonly=True)
        if self.request.has_perm('emailbounces.view'):
            g.viewable = True
            g.view_route_name = 'emailbounce'
        if self.request.has_perm('emailbounces.delete'):
            g.deletable = True
            g.delete_route_name = 'emailbounce.delete'
        return g


class LinksFieldRenderer(formalchemy.FieldRenderer):

    def render_readonly(self, **kwargs):
        value = self.raw_value
        if not value:
            return 'n/a'
        html = literal('<ul>')
        for link in value:
            html += literal('<li>{0}:&nbsp; <a href="{1}" target="_blank">{2}</a></li>'.format(
                link.type, link.url, link.title))
        html += literal('</ul>')
        return html


class EmailBounceCrud(CrudView):
    """
    Main CRUD view for email bounces.
    """
    mapped_class = model.EmailBounce
    home_route = 'emailbounces'
    pretty_name = "Email Bounce"

    def get_handler(self, bounce):
        return get_handler(self.rattail_config, bounce.config_key)

    def fieldset(self, bounce):
        assert isinstance(bounce, model.EmailBounce)
        handler = self.get_handler(bounce)
        fs = self.make_fieldset(bounce)
        fs.bounced.set(renderer=renderers.DateTimeFieldRenderer(self.rattail_config))
        fs.processed.set(renderer=renderers.DateTimeFieldRenderer(self.rattail_config))
        fs.append(formalchemy.Field('message',
                                    value=handler.msgpath(bounce),
                                    renderer=BounceMessageFieldRenderer.new(self.request, handler)))
        fs.append(formalchemy.Field('links',
                                    value=list(handler.make_links(Session(), bounce.intended_recipient_address)),
                                    renderer=LinksFieldRenderer))
        fs.configure(
            include=[
                fs.config_key.label("Source"),
                fs.message,
                fs.bounced,
                fs.bounce_recipient_address.label("Bounced To"),
                fs.intended_recipient_address.label("Intended For"),
                fs.links,
                fs.processed,
                fs.processed_by,
            ],
            readonly=True)
        if not bounce.processed:
            del fs.processed
            del fs.processed_by
        return fs

    def template_kwargs(self, form):
        kwargs = super(EmailBounceCrud, self).template_kwargs(form)
        bounce = form.fieldset.model
        handler = self.get_handler(bounce)
        kwargs['handler'] = handler
        with open(handler.msgpath(bounce), 'rb') as f:
            kwargs['message'] = f.read()
        return kwargs

    def process(self):
        """
        View for marking a bounce as processed.
        """
        bounce = self.get_model_from_request()
        if not bounce:
            return HTTPNotFound()
        bounce.processed = datetime.datetime.utcnow()
        bounce.processed_by = self.request.user
        self.request.session.flash("Email bounce has been marked processed.")
        return HTTPFound(location=self.request.route_url('emailbounces'))

    def unprocess(self):
        """
        View for marking a bounce as *unprocessed*.
        """
        bounce = self.get_model_from_request()
        if not bounce:
            return HTTPNotFound()
        bounce.processed = None
        bounce.processed_by = None
        self.request.session.flash("Email bounce has been marked UN-processed.")
        return HTTPFound(location=self.request.route_url('emailbounces'))

    def download(self):
        """
        View for downloading the message file associated with a bounce.
        """
        bounce = self.get_model_from_request()
        if not bounce:
            return HTTPNotFound()
        handler = self.get_handler(bounce)
        path = handler.msgpath(bounce)
        response = FileResponse(path, request=self.request)
        response.headers[b'Content-Length'] = str(os.path.getsize(path))
        response.headers[b'Content-Disposition'] = b'attachment; filename="bounce.eml"'
        return response


def add_routes(config):
    config.add_route('emailbounces', '/emailbounces/')
    config.add_route('emailbounce', '/emailbounces/{uuid}')
    config.add_route('emailbounce.process', '/emailbounces/{uuid}/process')
    config.add_route('emailbounce.unprocess', '/emailbounces/{uuid}/unprocess')
    config.add_route('emailbounce.delete', '/emailbounces/{uuid}/delete')
    config.add_route('emailbounce.download', '/emailbounces/{uuid}/download')


def includeme(config):
    add_routes(config)

    config.add_view(EmailBouncesGrid, route_name='emailbounces',
                    renderer='/emailbounces/index.mako',
                    permission='emailbounces.list')

    config.add_view(EmailBounceCrud, attr='read', route_name='emailbounce',
                    renderer='/emailbounces/crud.mako',
                    permission='emailbounces.view')

    config.add_view(EmailBounceCrud, attr='process', route_name='emailbounce.process',
                    permission='emailbounces.process')

    config.add_view(EmailBounceCrud, attr='unprocess', route_name='emailbounce.unprocess',
                    permission='emailbounces.unprocess')

    config.add_view(EmailBounceCrud, attr='download', route_name='emailbounce.download',
                    permission='emailbounces.download')

    config.add_view(EmailBounceCrud, attr='delete', route_name='emailbounce.delete',
                    permission='emailbounces.delete')
