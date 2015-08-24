def instance_required(f):
    def wrapped(self, *args, **kwargs):
        if self.instance is not None:
            return f(self, *args, **kwargs)
    return wrapped
