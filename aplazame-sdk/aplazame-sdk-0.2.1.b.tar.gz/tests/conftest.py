import pytest


@pytest.fixture(scope='class')
def conf_class(request):
    request.cls.host = request.config.option.host
    request.cls.private_token = request.config.option.private_token
    request.cls.public_token = request.config.option.public_token
    request.cls.api_version = request.config.option.api_version
    request.cls.verify = not request.config.option.skip_verify


def pytest_addoption(parser):
    parser.addoption(
        '--host',
        default='api.aplazame.com',
        help='API host server')

    parser.addoption(
        '--private-token',
        dest='private_token',
        help='Private Authorization token')

    parser.addoption(
        '--public-token',
        dest='public_token',
        help='Public Authorization token')

    parser.addoption(
        '--api-version',
        default=1,
        dest='api_version',
        help='API version')

    parser.addoption(
        '--skip-verify',
        action='store_true',
        default=False,
        dest='skip_verify',
        help='Skip ssl verification')
