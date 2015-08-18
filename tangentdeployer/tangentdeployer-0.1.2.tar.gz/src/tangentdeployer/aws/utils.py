from fabric.colors import green, red, yellow
from fabconfig import env


class DoesNotExist(Exception):
    pass


def message(color, msg):
    bar = '+' + '-' * (len(msg) + 2) + '+'
    print(color(''))
    print(color(bar))
    print(color("| %s |" % msg))
    print(color(bar))
    print(color(''))


def success(msg):
    message(green, msg)


def failure(msg):
    message(red, msg)


def status(msg):
    message(yellow, msg)


def get_app_user_data(env):
    user_data = open('bootstrap/app-user-data.sh').read()
    user_data = user_data.replace('{{ base_url }}', env.base_url)
    user_data = user_data.replace('{{ docker_host }}', env.docker_host)
    user_data = user_data.replace(
        '{{ app_docker_image }}', env.app_docker_image)
    user_data = user_data.replace(
        '{{ logstash_docker_image }}', env.logstash_docker_image)
    user_data = user_data.replace(
        '{{ nginx_docker_image }}', env.nginx_docker_image)
    user_data = user_data.replace(
        '{{ elasticsearch_host }}', env.elasticsearch_host)
    user_data = user_data.replace('{{ s3_path }}', env.s3_bootstrap_bucket)
    user_data = user_data.replace('{{ region }}', env.region)
    user_data = user_data.replace('{{ env }}', env.environment)
    user_data = user_data.replace('{{ basic_auth }}', env.basic_auth)
    user_data = user_data.replace(
        '{{ rabbitmq_docker_image }}', env.rabbitmq_docker_image)
    user_data = user_data.replace(
        '{{ memcached_docker_image }}', env.memcached_docker_image)
    user_data = user_data.replace(
        '{{ use_logstash }}', env.logstash_docker_image == '')
    user_data = user_data.replace(
        '{{ use_memcached }}', env.memcached_docker_image == '')
    user_data = user_data.replace(
        '{{ use_rabbitmq }}', env.rabbitmq_docker_image == '')
    return user_data


def get_logging_user_data(env):
    user_data = open('bootstrap/logging-user-data.sh').read()
    user_data = user_data.replace('{{ s3_path }}', env.s3_bootstrap_bucket)
    user_data = user_data.replace('{{ docker_host }}', env.docker_host)
    user_data = user_data.replace(
        '{{ kibana_docker_image }}', env.kibana_docker_image)
    user_data = user_data.replace(
        '{{ nginx_docker_image }}', env.nginx_docker_image)
    user_data = user_data.replace(
        '{{ elasticsearch_docker_image }}', env.elasticsearch_docker_image)
    user_data = user_data.replace('{{ region }}', env.region)
    user_data = user_data.replace('{{ env }}', env.environment)
    return user_data


def security_groups():
    security_groups = env.connections.ec2.get_all_security_groups(
        groupnames=env.security_groups)
    return [security_group.id for security_group in security_groups]
