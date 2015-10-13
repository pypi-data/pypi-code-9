import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import asbool
import jieba
import jieba.analyse
from ckan.plugins.toolkit import request, c
import pylons.config as config
import opencc

class Data_RecommendationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_recommendation')


    @classmethod
    def related_pkgs(cls):
        # Parameter
        extractNum = int(config.get('ckan.data_recommended.extract_num', '5'))
        byTag = asbool(config.get('ckan.data_recommended.by_tag', 'true'))
        byTitle = asbool(config.get('ckan.data_recommended.by_title', 'true'))

        # fetch pkg info
        pkg_name = request.environ['PATH_INFO'].split('/')[-1]
        pkg_title = toolkit.get_action('package_show')({}, {'id':pkg_name})['title']
        pkg_title_s = opencc.convert(pkg_title, config='zhtw2zhcn_s.ini')
        pkg_tags = [pkg_tag['name'] for pkg_tag in toolkit.get_action('package_show')({}, {'id':pkg_name})['tags']]

         # related_tag_titles
        related_tag_titles = set()
        if byTag:
            related_tag_titles.update(set(pkg_tags))

        if byTitle:
            tmp = jieba.analyse.extract_tags(pkg_title_s, topK=extractNum)
            related_tag_titles.update(
                set(
                    (opencc.convert(_, config='zhs2zhtw_vp.ini') for _ in tmp)
                )
            )

        related_pkgs = {}

        related_pkgs['results'] = dict()
        for related_tag_title in related_tag_titles:
            tmp = toolkit.get_action('package_search')({}, {'q': related_tag_title, 'rows': 20})
            related_pkg_results = tmp['results']
            related_pkgs['results'][related_tag_title] = dict()

            related_pkgs['results'][related_tag_title]['rows'] =  tmp['count']

            # filte the same title
            related_pkg_results = [_ for _ in related_pkg_results if _['title'] != pkg_title]
            related_pkgs['results'][related_tag_title]['result'] =  related_pkg_results

        # related_pkgs['results'][related_tag_title] = sorted(related_pkgs['results'][related_tag_title], key=lambda t: len(t))
        return related_pkgs

    def get_helpers(self):
        return {'related_pkgs': self.related_pkgs}