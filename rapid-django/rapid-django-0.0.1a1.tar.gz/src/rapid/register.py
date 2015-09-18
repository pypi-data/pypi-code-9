__author__ = 'marcos'

from rapid.views import bare_or_main, ListView, ReadView, UpdateView, CreateView, SelectView, DeleteView,\
    update_form_class
from rapid import permissions
from rapid.registry import Action, MenuEntry, registry


def _rvw(view_class, action_name):
    view_class.action_name = action_name

    def vw(model):
        return bare_or_main(view_class.as_view(model=model))
    return vw


_default_actions = [
    (False, Action("list", "", [], _rvw(ListView, 'list'), "listar", "fa-list")),
    (False, Action("view", "(?P<pk>[0-9]+)", ['pk'], _rvw(ReadView, 'view'), "ver", "fa-eye")),
    (True, Action("edit", "(?P<pk>[0-9]+)", ['pk'], _rvw(UpdateView, 'edit'), "editar", "fa-pencil")),
    (True, Action("add", "", [], _rvw(CreateView, 'add'), "adicionar", "fa-plus")),
    (False, Action("select", "", [], _rvw(SelectView, 'select'), "selecionar", "fa-hand-o-up",
                   visibility=Action.Visibility.hidden)),
]


def model(model, read_set, write_set, actions=None, url_name=None, can_erase=False):
    if actions:
        actions = [(edt, a) for edt, a in _default_actions if a.name in actions]
    else:
        actions = _default_actions
    ret = []
    for edt, a in actions:
        if edt:
            ret.append(registry.register_action(a, MenuEntry(model, write_set, url_name=url_name)))
        else:
            ret.append(registry.register_action(a, MenuEntry(model, read_set, url_name=url_name)))
    if can_erase:
        a =  Action("delete", "(?P<pk>[0-9]+)", ['pk'], _rvw(DeleteView, 'delete'), "apagar", "fa-trash-o")
        ret.append(registry.register_action(a, MenuEntry(model, write_set, url_name=url_name)))
    return [u for u in ret if u]


def instance_form(model, action_name, entry_name, form, permission_set, url_name=None, icon=None, visibility=None):
    if not icon:
        icon = ''
    a = Action(action_name, "(?P<pk>[0-9]+)", ['pk'], _rvw(update_form_class(form), action_name),
               entry_name, icon, visibility)
    u = registry.register_action(a, MenuEntry(model, permission_set, url_name=url_name))
    return [u] if u else []


def select(model, visible_fields, permission_set, url_name=None):
    class Vw(SelectView):
        fields = visible_fields
    a = Action("select", "", [], _rvw(Vw, 'select'), "selecionar", "fa-hand-o-up",
               visibility=Action.Visibility.hidden)
    u = registry.register_action(a, MenuEntry(model, permission_set, url_name=url_name))
    return [u] if u else []
