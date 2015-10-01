# encoding=utf-8

import functools
import jambalaya as ja
import utils


class browse_list_proxy(object):
    def __init__(self, cr, uid):
        self.models = utils.get_database_registry(cr.dbname)
        self.cr = cr
        self.uid = uid

    def __call__(self, browse_list):
        return browse_list_proxy_impl(self, browse_list)


class browse_list_proxy_impl(object):
    def __init__(self, proxy, browse_list):
        self.proxy = proxy
        self.browse_list = browse_list

    def __getattr__(self, name):
        val = getattr(self.rmodel, name)
        if callable(val):
            return functools.partial(val, *self.args)

        return val

    @ja.hacks.singleton
    def rmodel(self):
        return self.proxy.models.get(
            self.model_name,
        )

    @ja.hacks.singleton
    def model_name(self):
        return self.browse_list[0]._name

    @ja.hacks.singleton
    def ids(self):
        return [r.id for r in self.browse_list]

    @ja.hacks.singleton
    def args(self):
        return [self.proxy.cr, self.proxy.uid, self.ids]
