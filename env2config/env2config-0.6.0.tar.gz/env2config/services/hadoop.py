
import requests as r
from lxml import etree
from lxml.builder import E
from past.builtins import basestring

from env2config.interface import RewriteOriented
from env2config.conversions import dotted_lower
from env2config.util import create_logger

HADOOP_URL = "http://hadoop.apache.org/docs/r{version}/{config_path}"

logger = create_logger()


class HadoopDefinition(RewriteOriented):
    service_name = 'hadoop'

    def get_tags(self):
        return {
            'distribution': self.tags.get('distribution', 'apache')
        }

    def default_configs(self):
        distribution = self.get_tags()['distribution']
        assert distribution == 'apache', 'Only apache hadoop distribution is supported for now.'

        def loader(config_path):
            url = HADOOP_URL.format(version=self.version, config_path=config_path)
            response = r.get(url)

            if response.status_code == 200:
                text = response.text
                return text

            else:
                raise ValueError(url)

        return {
            'hdfs-site.xml': lambda: loader('hadoop-project-dist/hadoop-hdfs/hdfs-default.xml'),
            'yarn-site.xml': lambda: loader('hadoop-yarn/hadoop-yarn-common/yarn-default.xml'),
            'mapred-site.xml': lambda: loader('hadoop-mapreduce-client/hadoop-mapreduce-client-core/mapred-default.xml'),
        }

    def config_mapping(self):
        return {
            'hdfs-site.xml': '/etc/hadoop/conf/hdfs-site.xml',
            'yarn-site.xml': '/etc/hadoop/conf/yarn-site.xml',
            'mapred-site.xml': '/etc/hadoop/conf/mapred-site.xml',
        }

    def config_multiplex(self, config_name):
        split_point = config_name.find('_')
        prefix = config_name[:split_point]
        rest = config_name[split_point + 1:]

        config_file = {
            'HDFS': 'hdfs-site.xml',
            'YARN': 'yarn-site.xml',
            'MAPRED': 'mapred-site.xml',
        }[prefix]
        return config_file, rest

    def convert_name(self, config_value):
        return dotted_lower(config_value)

    def ignore_env_names(self):
        return [
            'HADOOP_VERSION',
            'HADOOP_URL',
            'HADOOP_HOME',
        ]

    def parse_file(self, text_content):
        xml = etree.XML(text_content)
        properties = xml.iter('property')

        def find_text(prop, elem_name):
            elem = prop.find(elem_name)
            if elem is None:
                return ''
            else:
                if elem.text is None:
                    return ''
                else:
                    return elem.text
        pairs = (
            (
                find_text(prop, 'name'),
                (find_text(prop, 'value'), find_text(prop, 'description'))
            ) for prop in properties
        )

        return dict(pairs)

    def inject_file(self, default_model, config_model):
        updated_model = dict(default_model, **config_model)

        properties = []
        for name, value_description in updated_model.items():
            if isinstance(value_description, basestring):
                value_description = (
                    value_description,
                    "Injected by env2config.  Default value was: {0}. Default description was: {1}".format(
                        default_model.get(name, ('', None))[0],
                        default_model.get(name, (None, ''))[1],
                    )
                )
            value, description = value_description
            properties.append(E.property(
                E.name(name),
                E.value(value),
                E.description(description),
            ))

        xml = E.configuration(*properties)
        xml_text = etree.tostring(xml, pretty_print=True, encoding='utf-8', xml_declaration=True)
        return xml_text
