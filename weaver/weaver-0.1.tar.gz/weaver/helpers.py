from fabric.api import env

def get_domain(domain):
    if domain == 'stage':
        return get_stage()
    elif domain == 'region':
        return get_region
    else:
        raise Exception("Invalid domain:%s" % domain)

def get_service():
    global env
    return env.service_registry.service

def get_region():
    global env
    return env.get('region', '')

def get_stage():
    global env
    return env.stage
