import os

import requests as r

from env2config.interface import LineOriented

DEFAULT_URL = \
    "https://raw.githubusercontent.com/apache/kafka/{version}/config/{filename}"


class KafkaDefinition(LineOriented):
    service_name = 'kafka'

    def get_tags(self):
        return {
            'scala': self.tags.get('scala', '2.11')
        }

    def default_configs(self):
        version = self.version

        def get_default(filename):
            url = DEFAULT_URL.format(version=version, filename=filename)
            response = r.get(url)

            if response.status_code == 200:
                text = response.text
                return text

            else:
                raise ValueError(version)

        return {
            'consumer.properties': lambda: get_default('consumer.properties'),
            'log4j.properties': lambda: get_default('log4j.properties'),
            'producer.properties': lambda: get_default('producer.properties'),
            'server.properties': lambda: get_default('server.properties'),
            'zookeeper.properties': lambda: get_default('zookeeper.properties'),
        }

    def config_mapping(self):
        scala_version = self.get_tags()['scala']

        root = '/opt/kafka_{scala_version}-{version}'.format(
            scala_version=scala_version,
            version=self.version
        )

        mapping = dict(
            (filename, os.path.join(root, 'config', filename))
            for filename in self.default_configs()
        )
        return mapping

    def config_multiplex(self, config_name):
        split_point = config_name.find('_')
        prefix = config_name[:split_point]
        rest = config_name[split_point + 1:]
        config_file = prefix.lower() + '.properties'
        return config_file, rest

    def ignore_env_names(self):
        return [
            'KAFKA_HOME',
        ]

    def convert_name(self, config_name):
        parts = config_name.split('_')
        formatted = '.'.join(p.lower() for p in parts)
        return formatted

    def convert_value(self, config_value):
        return config_value

    def match_line(self, line, config_name):
        content = line.replace('#', '').strip()
        matches = content.split('=')[0] == config_name
        return matches

    def inject_line(self, old_line, config_name, config_value):
        new_line = '{0}={1}\n'.format(config_name, config_value)
        return new_line

    def comment_line(self, content):
        return '# ' + content + '\n'

