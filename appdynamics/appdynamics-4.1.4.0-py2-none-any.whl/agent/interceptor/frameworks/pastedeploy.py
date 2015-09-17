import appdynamics.agent
from appdynamics.agent.interceptor.frameworks.wsgi import WSGIInterceptor, WSGIApplication


def composite_factory(loader, global_conf, target, **local_conf):
    target = loader.get_app(target, global_conf=global_conf)

    try:
        agent = appdynamics.agent.get_agent_instance()
        appdynamics.agent.configure(local_conf)

        interceptor = WSGIInterceptor(agent, WSGIApplication)
        interceptor.attach('wsgi_application', patched_method_name='application_callable')

        return WSGIApplication(application=target)
    except:
        return target
