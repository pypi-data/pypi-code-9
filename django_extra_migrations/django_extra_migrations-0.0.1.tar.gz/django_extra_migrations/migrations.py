from __future__ import unicode_literals
from django.contrib.auth.models import Group, Permission, PermissionManager
from django.contrib.contenttypes.models import ContentType
from django.db.migrations.operations.base import Operation
from django.db.models.loading import get_model
from progressbar import ProgressBar


class Resave(Operation):
    def __init__(self, model_path):
        self.model_path = model_path

    @property
    def reversible(self):
        return True

    def state_forwards(self, app_label, state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        model = get_model(self.model_path)
        ttl = model.objects.count()
        i = 0
        print "\n\tResave model %s. Total: %d" % (self.model_path, ttl)
        with ProgressBar(maxval=ttl) as p:
            for record in model.objects.all():
                record.save(force_update=True)
                i += 1
                p.update(i)

    def describe(self):
        return "Resave all records with calling save and signals events"


class GrantPermissions(Operation):
    def __init__(self, groups, perms):
        self.groups = groups
        self.perms = perms

    @property
    def reversible(self):
        return True

    def state_forwards(self, app_label, state):
        pass

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        for perm in self.prepare_perms():
            for group in Group.objects.filter(name__in=self.groups):
                group.permissions.add(perm)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        for perm in self.prepare_perms():
            for group in Group.objects.filter(name__in=self.groups):
                group.permissions.remove(perm)

    def prepare_perms(self):
        for model_path, perms in self.perms:
            ct = ContentType.objects.get_for_model(get_model(model_path))
            kw = {"content_type": ct}
            if perms is not True:
                kw['codename__in'] = perms

            for perm in Permission.objects.filter(**kw):
                yield perm

    def describe(self):
        return "Grant permissions to groups"
