__author__ = 'marcos.medeiros'


class Permission:
    """
    A permission for an registry entry.
    """
    def __init__(self, model, instances):
        self.model = model
        self.instances = instances


def all_instances(model):
    """
    Shortuct function for granting permission over all instances of a model.
    For that use, create a permission with this function at its "instances" attribute.
    """
    def i(request):
        if model(request):
            return {}
        else:
            return None
    return i


def apply_instances_permission(model, perm):
    """
    Returns the set of objects that a resolved permission has access to.
    :param model: ModelData of the model that'll be filtered
    :param perm: Resolved permission (that is, the result of evaluating permission.instances(request))
    """
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
    """
    Verifies if an object instance access is permited
    :param model: ModelData of the desired model
    :param perm: Resolved permission (that is, the result of evaluating permission.instances(request))
    :param instance: Instance that'll be verified.
    """
    p = apply_instances_permission(model, perm)
    if hasattr(p, 'filter'):
        return p.filter(pk=instance.pk).exists()
    if hasattr(p, '__iter__'):
        return bool([f for f in p if f.pk == instance.pk])
    return False


def to_profile(profile):
    """
    Grants permission over the model and all instances to the given profile(s)
    :param profile: A profile.id or an iterable of those.
    """
    if hasattr(profile, "__iter__"):
        def m(request):
            if not request.user.is_authenticated():
                return False
            up = [p.pk for p in request.user.profile_set]
            for p in up:
                if p in profile:
                    return True
            return False
    else:
        def m(request):
            if not request.user.is_authenticated():
                return False
            up = [p.pk for p in request.user.profile_set.all()]
            if profile in up:
                return True
            return False
    return Permission(m, all_instances(m))


def to_staff():
    """
    Grants permission over the model and all instances to every user with is_staff set.
    """
    def m(request):
        if request.user.is_authenticated() and request.user.is_staff:
            return True
        return False
    return Permission(m, all_instances(m))


def to_all():
    """
    Grants permission over the model and all instances to all users.
    """
    def m(request):
        return True
    return Permission(m, all_instances(m))


def to_superusers():
    """
    Grants permission over the model and all instances to every user with superuser set.
    """
    def m(request):
        if request.user.is_authenticated() and request.user.is_superuser:
            return True
        return False
    return Permission(m, all_instances(m))


def to_application_managers(app):
    """
    Grants permission over the model and all instances to the manager of the given application
    :param app: Application.id of the desired application
    """
    def m(request):
        if not request.user.is_authenticated():
            return False
        up = [a.pk for a in request.user.managed_applications.all()]
        if app in up:
            return True
        return False
    return Permission(m, all_instances(m))
