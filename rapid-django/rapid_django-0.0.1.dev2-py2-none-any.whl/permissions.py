__author__ = 'marcos.medeiros'

class Permission:
    def __init__(self, model, instances):
        self.model = model
        self.instances = instances

def all_instances(model):
    def i(request):
        if model(request):
            return {}
        else:
            return None
    return i

def apply_instances_permission(model, perm):
    if perm is None:
        return []
    if hasattr(perm, 'keys'):
        return model.default_manager().filter(**perm)
    if hasattr(perm, '__iter__'):
        return perm
    if hasattr(perm, 'all'):
        return perm
    return []

def has_instance(model, perm, instance):
    p = apply_instances_permission(model, perm)
    if hasattr(p, 'filter'):
        return p.filter(pk=instance.pk).exists()
    if hasattr(p, '__iter__'):
        return bool([f for f in p if f.pk == instance.pk])
    return False

def to_profile(profile):
    if hasattr(profile, "__iter__"):
        def m(request):
            if not request.user.is_authenticated():
                return False
            up = [p.pk for p in request.user.profile_set]
            for p in up:
                if p in profile:
                    True
            return False
    else:
        def m(request):
            if not request.user.is_authenticated():
                return False
            up = [p.pk for p in request.user.profile_set]
            if profile in up:
                return True
            return False
    return Permission(m, all_instances(m))

def to_staff():
    def m(request):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        return False
    return Permission(m, all_instances(m))

def to_all():
    def m(request):
        return True
    return Permission(m, all_instances(m))

def to_superusers():
    def m(request):
        if request.user.is_authenticated() and request.user.is_superuser:
            return True
        return False
    return Permission(m, all_instances(m))
