import requests as r

from env2config.interface import LineOriented
from env2config.conversions import dashed_lower

DEFAULT_URL = \
    'https://raw.githubusercontent.com/antirez/redis/{version}/redis.conf'


class RedisDefition(LineOriented):
    service_name = 'redis'

    def default_configs(self):
        version = self.version

        def get_default():
            url = DEFAULT_URL.format(version=version)
            response = r.get(url)

            if response.status_code == 200:
                text = response.text
                return text

            else:
                raise ValueError(version)

        return {
            'redis.conf': get_default
        }

    def config_mapping(self):
        return {
            'redis.conf': '/etc/redis.conf'
        }

    def ignore_env_names(self):
        return [
            'REDIS_DOWNLOAD_URL',
            'REDIS_DOWNLOAD_SHA1',
            'REDIS_VERSION',
            'REDIS_URL',
        ]

    def convert_name(self, config_name):
        return dashed_lower(config_name)

    def convert_value(self, config_value):
        return config_value

    def match_line(self, line, config_name):
        content = line.replace('#', '').strip()
        line_config = content.split(' ')[0]
        matches = (line_config == config_name)
        return matches

    def inject_line(self, old_line, config_name, config_value):
        new_line = '{0} {1}\n'.format(config_name, config_value)
        return new_line

    def comment_line(self, content):
        return '# ' + content + '\n'
