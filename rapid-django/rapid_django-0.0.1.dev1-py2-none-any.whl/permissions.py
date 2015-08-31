__author__ = 'marcos.medeiros'

from rapid import wrappers

def default_read(model):
    m = wrappers.ModelData(model)

    def perm(request):
        if request.user.is_authenticated() and request.user.is_staff():
            return m.default_manager()
        return None
    return perm

def default_write(model):
    def perm(request):
        return None
    return perm

def to_profile(model, profile):
    m = wrappers.ModelData(model)
    if hasattr(profile, "__iter__"):

        def perm(request):
            if not request.user.is_authenticated():
                return None
            up = [p.pk for p in request.user.profile_set]
            for p in up:
                if p in profile:
                    return m.default_manager()
            return None
        return perm

    def perm(request):
        if not request.user.is_authenticated():
            return None
        up = [p.pk for p in request.user.profile_set]
        if profile in up:
            return m.default_manager()
        return None
    return perm

def to_staff(model):
    m = wrappers.ModelData(model)

    def perm(request):
        if request.user.is_authenticated() and request.user.is_staff():
            return m.default_manager()
        return None
    return perm

def to_all(model):
    m = wrappers.ModelData(model)

    def perm(request):
        return m.default_manager()
    return perm

def to_admins(model):
    m = wrappers.ModelData(model)

    def perm(request):
        if request.user.is_authenticated() and request.user.is_admin():
            return m.default_manager()
        return None
    return perm
