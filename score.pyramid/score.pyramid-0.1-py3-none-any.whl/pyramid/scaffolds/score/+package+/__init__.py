from score.init.pyramid import init_from_file as init_score


def init(file):
    """
    Initializes the application and returns a pyramid configuration, as well
    as the score configuration.
    """
    config, score = init_score(file)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('dev/checklist', '/')
    config.add_route('dev/checklist/ajax', '/_dev/checklist/{command}')
    config.scan()
    return config, score


def main(global_config, **settings):
    """
    Calls :func:`.init` and returns a WSGI application.
    """
    config, score = init(global_config['__file__'])
    return config.make_wsgi_app()
