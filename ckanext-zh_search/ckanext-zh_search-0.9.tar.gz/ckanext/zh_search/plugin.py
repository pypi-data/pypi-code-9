# -*- coding: utf8 -*-

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import jieba
import opencc

class Zh_SearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'zh_search')

    # IPackageController

    def before_search(self, search_params):
        if search_params.has_key('q'):
            if 'owner_org:' not in search_params['q']:
                q = search_params['q']
                q = opencc.convert(q, config='zhtw2zhcn_s.ini')
                search_params['q'] = u" ".join(jieba.cut(q))
                # print search_params['q']
        return search_params

    def before_index(self, pkg_dict):
        title = pkg_dict['title']
        title = opencc.convert(title, config='zhtw2zhcn_s.ini')
        seg_list = jieba.cut_for_search(title)
        pkg_dict['title'] = " ".join(seg_list)
        return pkg_dict