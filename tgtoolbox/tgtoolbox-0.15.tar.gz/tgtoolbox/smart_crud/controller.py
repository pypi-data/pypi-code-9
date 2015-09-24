# -*- coding: utf-8 -*-
from tg import request, redirect, expose, tmpl_context, response, abort
from tg.decorators import without_trailing_slash, before_validate, with_trailing_slash
from tgext.crud.controller import CrudRestController, errors
from tgext.crud.utils import create_setter, map_args_to_pks, allow_json_parameters, force_response_type
from tgext.crud.decorators import registered_validate, catch_errors
from sprox.fillerbase import RecordFiller, AddFormFiller
from .table import SmartTable
from .form import SmartAddForm, SmartEditForm
from .pagination import SmartPaginate as paginate
__author__ = 'vahid'


class SmartCrudRestController(CrudRestController):
    model = None
    pagination = False
    menu_items = []
    allow_new = True
    allow_delete = True
    allow_edit = True
    limit_max_rows = None
    limit_min_rows = None

    def __init__(self, session, menu_items=None):
        self.session = session
        if menu_items:
            self.menu_items = menu_items

        if not (hasattr(self, 'table') or hasattr(self, 'table_type')):
            class Table(SmartTable):
                __entity__ = self.model
                allow_new = self.allow_new
                allow_delete = self.allow_delete
                allow_edit = self.allow_edit
                limit_max_rows = self.limit_max_rows
                limit_min_rows = self.limit_min_rows

            self.table = Table(session)

        if self.allow_edit:
            if not (hasattr(self, 'edit_form') or hasattr(self, 'edit_form_type')):
                class EditForm(SmartEditForm):
                    __entity__ = self.model
                self.edit_form = EditForm(session)

            if not (hasattr(self, 'edit_filler') or hasattr(self, 'edit_filler_type')):
                class EditFiller(RecordFiller):
                    __entity__ = self.model
                self.edit_filler = EditFiller(session)
        else:
            self.edit_form = None
            self.edit_filler = None

        if self.allow_new:
            if not (hasattr(self, 'new_form') or hasattr(self, 'new_form_type')):
                class NewForm(SmartAddForm):
                    __entity__ = self.model
                self.new_form = NewForm(session)

            if not (hasattr(self, 'new_filler') or hasattr(self, 'new_filler_type')):
                class NewFiller(AddFormFiller):
                    __entity__ = self.model
                self.new_filler = NewFiller(session)
        else:
            self.new_form = None
            self.new_filler = None

        super(SmartCrudRestController, self).__init__(session, menu_items)

        #Permit to quickly customize form options
        if hasattr(self, '__form_options__'):
            for name, value in self.__form_options__.items():
                for form in (self.edit_form, self.new_form):
                    if form:
                        setattr(form, name, value)

        #Permit to quickly create custom actions to set values
        if hasattr(self, '__setters__'):
            for name, config in self.__setters__.items():
                setattr(self, name, create_setter(self, self.get_all, config))


        #Permit to quickly customize table options
        if hasattr(self, '__table_options__'):
            for name, value in self.__table_options__.items():
                setattr(self.table, name, value)

    def _before(self, *args, **kw):
        tmpl_context.title = self.title
        tmpl_context.menu_items = self.menu_items
        tmpl_context.kept_params = self._kept_params()
        tmpl_context.crud_helpers = self.helpers
        tmpl_context.model_name = self.model.__name__

        for resource in self.resources:
            resource.inject()
        force_response_type(self.response_type)

    def _adapt_menu_items(self, menu_items):
        if hasattr(self, 'menu_items'):
            return self.menu_items
        return menu_items

    def select_query(self):
        return self.session.query(self.model)

    @with_trailing_slash
    @expose('tgtoolbox.smart_crud.templates.list')
    @paginate(items_per_page=20)
    def get_all(self, *args, **kw):
        self.table.query = self.select_query()
        tmpl_context.table = self.table
        return dict(data=self.table.query)

    @expose('mako:tgtoolbox.smart_crud.templates.view')
    @expose('json:')
    def get_one(self, *args, **kw):
        """get one record, returns HTML or json"""
        #this would probably only be realized as a json stream
        kw = map_args_to_pks(args, {})

        if request.response_type == 'application/json':
            obj = self.provider.get_obj(self.model, kw)
            if obj is None:
                response.status_code = 404
            elif self.conditional_update_field is not None:
                response.last_modified = getattr(obj, self.conditional_update_field)

            return dict(model=self.model.__name__,
                        value=self._dictify(obj))

        tmpl_context.widget = self.edit_form
        value = self.edit_filler.get_value(kw)
        return dict(value=value, model=self.model.__name__)

    @expose('mako:tgtoolbox.smart_crud.templates.edit')
    def edit(self, *args, **kw):
        """Display a page to edit the record."""
        if not self.allow_edit:
            abort(404)
        pks = self.provider.get_primary_fields(self.model)
        kw = map_args_to_pks(args, {})

        tmpl_context.widget = self.edit_form
        value = self.edit_filler.get_value(kw)
        value['_method'] = 'PUT'
        return dict(value=value, model=self.model.__name__, pk_count=len(pks))

    @without_trailing_slash
    @expose('mako:tgtoolbox.smart_crud.templates.new')
    def new(self, *args, **kw):
        """Display a page to show a new record."""
        if not self.allow_new:
            abort(404)
        tmpl_context.widget = self.new_form
        return dict(value=kw, model=self.model.__name__)

    @expose(content_type='text/html')
    @expose('json:', content_type='application/json')
    @before_validate(allow_json_parameters)
    @catch_errors(errors, error_handler=new)
    @registered_validate(error_handler=new)
    def post(self, *args, **kw):
        if not self.allow_new:
            abort(404)
        obj = self.provider.create(self.model, params=kw)
        if request.response_type == 'application/json':
            if obj is not None and self.conditional_update_field is not None:
                response.last_modified = getattr(obj, self.conditional_update_field)

            return dict(model=self.model.__name__,
                        value=self._dictify(obj))

        return redirect('./', params=self._kept_params())

    @expose(content_type='text/html')
    @expose('json:', content_type='application/json')
    @before_validate(allow_json_parameters)
    @before_validate(map_args_to_pks)
    @registered_validate(error_handler=edit)
    @catch_errors(errors, error_handler=edit)
    def put(self, *args, **kw):
        """update"""
        if not self.allow_edit:
            abort(404)
        omit_fields = []
        if getattr(self, 'edit_form', None):
            omit_fields.extend(self.edit_form.__omit_fields__)

        for remembered_value in self.remember_values:
            value = kw.get(remembered_value)
            if value is None or value == '':
                omit_fields.append(remembered_value)

        obj = self.provider.get_obj(self.model, kw)

        #This should actually by done by provider.update to make it atomic
        can_modify = True
        if obj is not None and self.conditional_update_field is not None and \
           request.if_unmodified_since is not None and \
           request.if_unmodified_since < getattr(obj, self.conditional_update_field):
                can_modify = False

        if obj is not None and can_modify:
            obj = self.provider.update(self.model, params=kw, omit_fields=omit_fields)

        if request.response_type == 'application/json':
            if obj is None:
                response.status_code = 404
            elif can_modify is False:
                response.status_code = 412
            elif self.conditional_update_field is not None:
                response.last_modified = getattr(obj, self.conditional_update_field)

            return dict(model=self.model.__name__,
                        value=self._dictify(obj))

        pks = self.provider.get_primary_fields(self.model)
        return redirect('../' * len(pks), params=self._kept_params())

    @expose(content_type='text/html')
    @expose('json:', content_type='application/json')
    def post_delete(self, *args, **kw):
        """This is the code that actually deletes the record"""
        if not self.allow_delete:
            abort(404)
        kw = map_args_to_pks(args, {})

        obj = None
        if kw:
            obj = self.provider.get_obj(self.model, kw)

        if obj is not None:
            self.provider.delete(self.model, kw)

        if request.response_type == 'application/json':
            return dict()

        pks = self.provider.get_primary_fields(self.model)
        return redirect('./' + '../' * (len(pks) - 1), params=self._kept_params())

    @expose('mako:tgtoolbox.smart_crud.templates.delete_confirm')
    def get_delete(self, *args, **kw):
        """This is the code that creates a confirm_delete page"""
        if not self.allow_delete:
            abort(404)
        return dict(args=args)