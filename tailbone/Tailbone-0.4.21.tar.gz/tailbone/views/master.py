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
Model Master View
"""

from __future__ import unicode_literals

import sqlalchemy as sa
from sqlalchemy import orm

from edbob.util import prettify

import formalchemy
from pyramid.renderers import get_renderer, render_to_response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from tailbone.db import Session
from tailbone.views import View
from tailbone.newgrids import filters, AlchemyGrid, GridAction
from tailbone.forms import AlchemyForm


class MasterView(View):
    """
    Base "master" view class.  All model master views should derive from this.
    """
    creatable = True
    viewable = True
    editable = True
    deletable = True

    creating = False
    viewing = False
    editing = False
    deleting = False

    row_attrs = {}
    cell_attrs = {}

    ##############################
    # Available Views
    ##############################

    def index(self):
        """
        View to list/filter/sort the model data.

        If this view receives a non-empty 'partial' parameter in the query
        string, then the view will return the renderered grid only.  Otherwise
        returns the full page.
        """
        grid = self.make_grid()

        # If user just refreshed the page with a reset instruction, issue a
        # redirect in order to clear out the query string.
        if self.request.GET.get('reset-to-default-filters') == 'true':
            return self.redirect(self.request.current_route_url(_query=None))

        if self.request.params.get('partial'):
            self.request.response.content_type = b'text/html'
            self.request.response.text = grid.render_grid()
            return self.request.response
        return self.render_to_response('index', {'grid': grid})

    def create(self):
        """
        View for creating a new model record.
        """
        self.creating = True
        form = self.make_form(self.model_class)
        if self.request.method == 'POST':
            if form.validate():
                form.save()
                instance = form.fieldset.model
                self.after_create(instance)
                self.request.session.flash("{0} {1} has been created.".format(
                    self.get_model_title(), instance))
                return HTTPFound(location=self.get_action_url('view', instance))
        return self.render_to_response('create', {'form': form})

    def view(self):
        """
        View for viewing details of an existing model record.
        """
        self.viewing = True
        instance = self.get_instance()
        form = self.make_form(instance)
        return self.render_to_response('view', {
            'instance': instance, 'form': form})

    def edit(self):
        """
        View for editing an existing model record.
        """
        self.editing = True
        instance = self.get_instance()
        form = self.make_form(instance)
        if self.request.method == 'POST':
            if form.validate():
                form.save()
                self.after_edit(instance)
                self.request.session.flash("{0} {1} has been updated.".format(
                    self.get_model_title(), instance))
                return HTTPFound(location=self.get_action_url('view', instance))
        return self.render_to_response('edit', {'instance': instance, 'form': form})

    def delete(self):
        """
        View for deleting an existing model record.
        """
        self.deleting = True
        instance = self.get_instance()

        # Let derived classes prep for (or cancel) deletion.
        result = self.before_delete(instance)
        if result is not None:
            return result

        self.delete_instance(instance)
        self.request.session.flash("{0} {1} has been deleted.".format(
            self.get_model_title(), instance))
        return self.redirect(self.get_after_delete_url(instance))


    ##############################
    # Core Stuff
    ##############################

    @classmethod
    def get_model_class(cls):
        """
        Returns the data model class for which the master view exists.
        """
        if not hasattr(cls, 'model_class'):
            raise NotImplementedError("You must define the `model_class` for: {0}".format(cls))
        return cls.model_class

    @classmethod
    def get_normalized_model_name(cls):
        """
        Returns the "normalized" name for the view's model class.  This will be
        the value of the :attr:`normalized_model_name` attribute if defined;
        otherwise it will be a simple lower-cased version of the associated
        model class name.
        """
        return getattr(cls, 'normalized_model_name', cls.get_model_class().__name__.lower())

    @classmethod
    def get_model_key(cls):
        """
        Return a string name for the primary key of the model class.
        """
        if hasattr(cls, 'model_key'):
            return cls.model_key
        mapper = orm.class_mapper(cls.get_model_class())
        return ','.join([k.key for k in mapper.primary_key])

    @classmethod
    def get_model_title(cls):
        """
        Return a "humanized" version of the model name, for display in templates.
        """
        return getattr(cls, 'model_title', cls.model_class.__name__)

    @classmethod
    def get_model_title_plural(cls):
        """
        Return a "humanized" (and plural) version of the model name, for
        display in templates.
        """
        return getattr(cls, 'model_title_plural', '{0}s'.format(cls.get_model_title()))

    @classmethod
    def get_route_prefix(cls):
        """
        Returns a prefix which (by default) applies to all routes provided by
        the master view class.  This is the plural, lower-cased name of the
        model class by default, e.g. 'products'.
        """
        model_name = cls.get_normalized_model_name()
        return getattr(cls, 'route_prefix', '{0}s'.format(model_name))

    @classmethod
    def get_url_prefix(cls):
        """
        Returns a prefix which (by default) applies to all URLs provided by the
        master view class.  By default this is the route prefix, preceded by a
        slash, e.g. '/products'.
        """
        return getattr(cls, 'url_prefix', '/{0}'.format(cls.get_route_prefix()))

    @classmethod
    def get_template_prefix(cls):
        """
        Returns a prefix which (by default) applies to all templates required by
        the master view class.  This uses the URL prefix by default.
        """
        return getattr(cls, 'template_prefix', cls.get_url_prefix())

    @classmethod
    def get_permission_prefix(cls):
        """
        Returns a prefix which (by default) applies to all permissions leveraged by
        the master view class.  This uses the route prefix by default.
        """
        return getattr(cls, 'permission_prefix', cls.get_route_prefix())

    def get_index_url(self):
        """
        Returns the master view's index URL.
        """
        return self.request.route_url(self.get_route_prefix())

    def get_action_url(self, action, instance):
        """
        Generate a URL for the given action on the given instance.
        """
        return self.request.route_url('{0}.{1}'.format(self.get_route_prefix(), action),
                                      **self.get_action_route_kwargs(instance))

    def render_to_response(self, template, data):
        """
        Return a response with the given template rendered with the given data.
        Note that ``template`` must only be a "key" (e.g. 'index' or 'view').
        First an attempt will be made to render using the :attr:`template_prefix`.
        If that doesn't work, another attempt will be made using '/master' as
        the template prefix.
        """
        data.update({
            'master': self,
            'model_title': self.get_model_title(),
            'model_title_plural': self.get_model_title_plural(),
            'route_prefix': self.get_route_prefix(),
            'permission_prefix': self.get_permission_prefix(),
            'index_url': self.get_index_url(),
            'action_url': self.get_action_url,
        })
        data.update(self.template_kwargs(**data))
        if hasattr(self, 'template_kwargs_{0}'.format(template)):
            data.update(getattr(self, 'template_kwargs_{0}'.format(template))(**data))
        try:
            return render_to_response('{0}/{1}.mako'.format(self.get_template_prefix(), template),
                                      data, request=self.request)
        except IOError:
            return render_to_response('/master/{0}.mako'.format(template),
                                      data, request=self.request)

    def template_kwargs(self, **kwargs):
        """
        Supplement the template context, for all views.
        """
        return kwargs

    def redirect(self, url):
        """
        Convenience method to return a HTTP 302 response.
        """
        return HTTPFound(location=url)

    ##############################
    # Grid Stuff
    ##############################

    @classmethod
    def get_grid_factory(cls):
        """
        Returns the grid factory or class which is to be used when creating new
        grid instances.
        """
        return getattr(cls, 'grid_factory', AlchemyGrid)

    @classmethod
    def get_grid_key(cls):
        """
        Returns the unique key to be used for the grid, for caching sort/filter
        options etc.
        """
        return getattr(cls, 'grid_key', '{0}s'.format(cls.get_normalized_model_name()))

    def make_grid_kwargs(self):
        """
        Return a dictionary of kwargs to be passed to the factory when creating
        new grid instances.
        """
        return {
            'width': 'full',
            'filterable': True,
            'sortable': True,
            'default_sortkey': getattr(self, 'default_sortkey', None),
            'sortdir': getattr(self, 'sortdir', 'asc'),
            'pageable': True,
            'main_actions': self.get_main_actions(),
            'more_actions': self.get_more_actions(),
            'checkbox': self.checkbox,
            'checked': self.checked,
            'row_attrs': self.get_row_attrs,
            'cell_attrs': self.get_cell_attrs,
            'model_title': self.get_model_title(),
            'model_title_plural': self.get_model_title_plural(),
            'permission_prefix': self.get_permission_prefix(),
            'route_prefix': self.get_route_prefix(),
        }

    def get_row_attrs(self, row, i):
        """
        Returns a dict of HTML attributes which is to be applied to the row's
        ``<tr>`` element.  Note that ``i`` will be a 1-based index value for
        the row within its table.  The meaning of ``row`` is basically not
        defined; it depends on the type of data the grid deals with.
        """
        if callable(self.row_attrs):
            return self.row_attrs(row, i)
        return self.row_attrs

    def get_cell_attrs(self, row, column):
        """
        Returns a dictionary of HTML attributes which should be applied to the
        ``<td>`` element in which the given row and column "intersect".
        """
        if callable(self.cell_attrs):
            return self.cell_attrs(row, column)
        return self.cell_attrs

    def get_main_actions(self):
        """
        Return a list of 'main' actions for the grid.
        """
        actions = []
        if self.viewable:
            actions.append(self.make_action('view', icon='zoomin'))
        return actions

    def get_more_actions(self):
        """
        Return a list of 'more' actions for the grid.
        """
        actions = []
        if self.editable:
            actions.append(self.make_action('edit', icon='pencil'))
        if self.deletable:
            actions.append(self.make_action('delete', icon='trash'))
        return actions

    def make_action(self, key, **kwargs):
        """
        Make a new :class:`GridAction` instance for the current grid.
        """
        kwargs.setdefault('url', lambda r: self.request.route_url(
            '{0}.{1}'.format(self.get_route_prefix(), key),
            **self.get_action_route_kwargs(r)))
        return GridAction(key, **kwargs)

    def get_action_route_kwargs(self, row):
        """
        Hopefully generic kwarg generator for basic action routes.
        """
        mapper = orm.object_mapper(row)
        keys = [k.key for k in mapper.primary_key]
        values = [getattr(row, k) for k in keys]
        return dict(zip(keys, values))

    def make_grid(self):
        """
        Make and return a new (configured) grid instance.
        """
        factory = self.get_grid_factory()
        key = self.get_grid_key()
        data = self.make_query()
        kwargs = self.make_grid_kwargs()
        grid = factory(key, self.request, data=data, model_class=self.model_class, **kwargs)
        grid._fa_grid.prettify = prettify
        self.configure_grid(grid)
        grid.load_settings()
        return grid

    def configure_grid(self, grid):
        """
        Configure the grid, customizing as necessary.  Subclasses are
        encouraged to override this method.

        As a bare minimum, the logic for this method must at some point invoke
        the ``configure()`` method on the grid instance.  The default
        implementation does exactly (and only) this, passing no arguments.
        This requirement is a result of using FormAlchemy under the hood, and
        it is in fact a call to :meth:`formalchemy:formalchemy.tables.Grid.configure()`.
        """
        grid.configure()

    def make_query(self, session=None):
        """
        Make the base query to be used for the grid.  Subclasses should not
        override this method; override :meth:`query()` instead.
        """
        if session is None:
            session = Session()
        return self.query(session)

    def query(self, session):
        """
        Produce the initial/base query for the master grid.  By default this is
        simply a query against the model class, but you may override as
        necessary to apply any sort of pre-filtering etc.  This is useful if
        say, you don't ever want to show records of a certain type to non-admin
        users.  You would modify the base query to hide what you wanted,
        regardless of the user's filter selections.
        """
        return session.query(self.model_class)

    def checkbox(self, instance):
        """
        Returns a boolean indicating whether ot not a checkbox should be
        rendererd for the given row.  Default implementation returns ``True``
        in all cases.
        """
        return True

    def checked(self, instance):
        """
        Returns a boolean indicating whether ot not a checkbox should be
        checked by default, for the given row.  Default implementation returns
        ``False`` in all cases.
        """
        return False

    ##############################
    # CRUD Stuff
    ##############################

    def get_instance(self):
        """
        Fetch the current model instance by inspecting the route kwargs and
        doing a database lookup.  If the instance cannot be found, raises 404.
        """
        key = self.request.matchdict[self.get_model_key()]
        instance = Session.query(self.model_class).get(key)
        if not instance:
            raise HTTPNotFound()
        return instance

    def make_form(self, instance, **kwargs):
        """
        Make a FormAlchemy-based form for use with CRUD views.
        """
        # TODO: Some hacky stuff here, to accommodate old form cruft.  Probably
        # should refactor forms soon too, but trying to avoid it for the moment.

        kwargs.setdefault('creating', self.creating)
        kwargs.setdefault('editing', self.editing)

        fieldset = self.make_fieldset(instance)
        self.configure_fieldset(fieldset)

        kwargs.setdefault('action_url', self.request.current_route_url(_query=None))
        if self.creating:
            kwargs.setdefault('cancel_url', self.get_index_url())
        else:
            kwargs.setdefault('cancel_url', self.get_action_url('view', instance))
        form = AlchemyForm(self.request, fieldset, **kwargs)
        form.readonly = self.viewing
        return form

    def make_fieldset(self, instance, **kwargs):
        """
        Make a FormAlchemy fieldset for the given model instance.
        """
        kwargs.setdefault('session', Session())
        kwargs.setdefault('request', self.request)
        fieldset = formalchemy.FieldSet(instance, **kwargs)
        fieldset.prettify = prettify
        return fieldset

    def configure_fieldset(self, fieldset):
        """
        Configure the given fieldset.
        """
        fieldset.configure()

    def after_create(self, instance):
        """
        Event hook, called just after a new instance is saved.
        """

    def after_edit(self, instance):
        """
        Event hook, called just after an existing instance is saved.
        """

    def deletable_instance(self, instance):
        """
        Returns boolean indicating whether or not the given instance can be
        considered "deletable".  Returns ``True`` by default; override as
        necessary.
        """
        return True

    def before_delete(self, instance):
        """
        Event hook, called just before deletion is attempted.
        """

    def delete_instance(self, instance):
        """
        Delete the instance, or mark it as deleted, or whatever you need to do.
        """
        # Flush immediately to force any pending integrity errors etc.; that
        # way we don't set flash message until we know we have success.
        Session.delete(instance)
        Session.flush()

    def get_after_delete_url(self, instance):
        """
        Returns the URL to which the user should be redirected after
        successfully "deleting" the given instance.
        """
        if hasattr(self, 'after_delete_url'):
            if callable(self.after_delete_url):
                return self.after_delete_url(instance)
            return self.after_delete_url
        return self.get_index_url()

    ##############################
    # Config Stuff
    ##############################

    @classmethod
    def defaults(cls, config):
        """
        Provide default configuration for a master view.
        """
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_key = cls.get_model_key()
        model_title = cls.get_model_title()
        model_title_plural = cls.get_model_title_plural()

        config.add_tailbone_permission_group(permission_prefix, model_title_plural)

        # list/search
        config.add_route(route_prefix, '{0}/'.format(url_prefix))
        config.add_view(cls, attr='index', route_name=route_prefix,
                        permission='{0}.list'.format(permission_prefix))
        config.add_tailbone_permission(permission_prefix, '{0}.list'.format(permission_prefix),
                                       "List/Search {0}".format(model_title_plural))

        # create
        if cls.creatable:
            config.add_route('{0}.create'.format(route_prefix), '{0}/new'.format(url_prefix))
            config.add_view(cls, attr='create', route_name='{0}.create'.format(route_prefix),
                            permission='{0}.create'.format(permission_prefix))
            config.add_tailbone_permission(permission_prefix, '{0}.create'.format(permission_prefix),
                                           "Create new {0}".format(model_title))

        # view
        if cls.viewable:
            config.add_route('{0}.view'.format(route_prefix), '{0}/{{{1}}}'.format(url_prefix, model_key))
            config.add_view(cls, attr='view', route_name='{0}.view'.format(route_prefix),
                            permission='{0}.view'.format(permission_prefix))
            config.add_tailbone_permission(permission_prefix, '{0}.view'.format(permission_prefix),
                                           "View {0} Details".format(model_title))

        # edit
        if cls.editable:
            config.add_route('{0}.edit'.format(route_prefix), '{0}/{{{1}}}/edit'.format(url_prefix, model_key))
            config.add_view(cls, attr='edit', route_name='{0}.edit'.format(route_prefix),
                            permission='{0}.edit'.format(permission_prefix))
            config.add_tailbone_permission(permission_prefix, '{0}.edit'.format(permission_prefix),
                                           "Edit {0}".format(model_title))

        # delete
        if cls.deletable:
            config.add_route('{0}.delete'.format(route_prefix), '{0}/{{{1}}}/delete'.format(url_prefix, model_key))
            config.add_view(cls, attr='delete', route_name='{0}.delete'.format(route_prefix),
                            permission='{0}.delete'.format(permission_prefix))
            config.add_tailbone_permission(permission_prefix, '{0}.delete'.format(permission_prefix),
                                           "Delete {0}".format(model_title))
