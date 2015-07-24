from django.db.models import *
from django.utils.text import slugify
from django.utils.timezone import now
from django.core.files.base import File
from django.dispatch import receiver

from rpy2.robjects.vectors import Vector

import os
import sys

from .settings import DATABASES, LIB_PATH
from .core import *

__all__ = ('AvailableLibrary', 'UploadedModule', 'UploadedScript', 'ScriptResult', 'ResultFile')

class LibraryManager(Manager):
    def refresh(self):
        for (name, version, location) in AvailableLibrary.PACKAGES.installed():
            goc = self.get_or_create(name=name, location=location,
                    defaults=dict(installed=now(), scheduled=False))
            goc[0].version = version
            goc[0].save()

class AvailableLibrary(Model):
    PACKAGES  = Packages()

    name      = CharField(max_length=32, choices=PACKAGES)
    version   = CharField(max_length=12, null=True, blank=True)
    location  = CharField(max_length=255, default="unknown")
    installed = DateTimeField(null=True, blank=True)
    attempted = DateTimeField(null=True, blank=True)
    scheduled = BooleanField("Schedule Install", default=True)

    objects = LibraryManager()

    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'
        unique_together = ('name', 'location')

    def __str__(self):
        (a, b) = (bool(self.installed), bool(self.attempted))
        if self.location[0] == '/' and \
           self.location.rstrip('/') != LIB_PATH.rstrip('/'):
            msg = 'system lib'
        else:
            msg = [['not installed', 'failed install'],
                   ['manual install', 'installed']][a][b]

        if self.scheduled:
            msg = 'scheduled'

        version = self.version + ' ' if self.version else ''
        return "%s (%s%s)" % (self.name, version, msg)

    def is_installed(self):
        return bool(self.installed)
    is_installed.boolean = True

    def install(self):
        self.attempted = now()
        self.scheduled = False
        if Library().install(self.name):
            self.installed = now()
            self.location = LIB_PATH
        self.save()
        return bool(self.installed)

    def uninstall(self, keep=True):
        Library().uninstall(self.name)
        if keep:
            self.installed = None
            self.location = 'deleted'
            self.save()


@receiver(signals.pre_delete, sender=AvailableLibrary, dispatch_uid='dellib')
def delete_lib(sender, instance, using, **kwargs):
    instance.uninstall(keep=False)


class UploadedModule(Model):
    name     = CharField(max_length=64)
    r_script = FileField('R Script', upload_to='rpy/modules/')

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def __str__(self):
        return self.name


DB_CHOICES = [ (db, db) for db in DATABASES.keys() ]

class UploadedScript(Model):
    name  = CharField(max_length=64)
    slug  = SlugField(max_length=64)

    libs  = ManyToManyField(AvailableLibrary, verbose_name='Libraries',
        null=True, blank=True, limit_choices_to={'installed__isnull': False})

    modules = ManyToManyField(UploadedModule, null=True, blank=True,
       help_text="""Optional modules to use in this script.""")

    db    = CharField('Database', max_length=32, choices=DB_CHOICES, null=True, blank=True)

    rsc   = TextField('R Script', help_text="""Use data sources:

      Uploaded CSV Data is available as 'csv'
      Website databases available as 'default' or name of database.
      Output filename is 'filename'.
    """)
    csv   = FileField('CSV Data', upload_to='rpy/csv/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Script'
        verbose_name_plural = 'Scripts'

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(unicode(self.name))
        return super(UploadedScript, self).save()

    def get_libs(self):
        libs = Library()
        for lib in self.libs.filter(installed__isnull=False):
            try:
                libs.append(lib.name)
            except ImportError:
                lib.installed = None
                lib.save()
        return libs

    def get_mods(self):
        for m in self.modules.all():
            yield m.r_script.path

    def run(self, **variables):
        result = self.results.create()
        result.started = now()
        result.save()

        runner = ScriptRunner(libs=self.get_libs(), modules=self.get_mods())

        if self.db:
            runner.use_database(self.db)

        try:
            ret = runner.run(str(self.rsc).replace('\r',''), **variables)
        except Exception as error:
            result.error = True
            result.result = str(error)
        else:
            if isinstance(ret, Vector):
                if len(ret) == 1:
                    ret = str(ret[0])
                else:
                    ret = str(list(ret))
            else:
                ret = str(ret)
            result.result = ret

        result.add_file(runner.filename)
        for filename in runner.filenames:
            result.add_file(filename)

        result.output = runner.r.out
        result.ended = now()
        result.save()

        return result


class ScriptResult(Model):
    script = ForeignKey(UploadedScript, related_name='results')

    started = DateTimeField(null=True, blank=True)
    ended   = DateTimeField(null=True, blank=True)

    output = TextField('Printed to Screen', null=True, blank=True)
    result = TextField('Result or Error', null=True, blank=True)
    error  = BooleanField(default=False)

    class Meta:
        ordering = ('-started',)
        verbose_name = 'Result'
        verbose_name_plural = 'Results'

    @property
    def fn_out(self):
       """Backwards compatibility"""
       if self.files.count() > 0:
           return self.files.all()[0].fn
       return None

    def add_file(self, filepath, order=-1):
        filename = os.path.basename(filepath)
        if not os.path.isfile(filepath):
            return
        if '_' in filename and order == -1:
            item = filename.rsplit('.', 1)[0].rsplit('_', 1)[-1]
            try:
                order = int(item)
            except:
                pass
        with open(filepath, 'r') as fhl:
            self.files.create(fn='-', order=order).save(filename, File(fhl))
        os.unlink(filepath)

    def __str__(self):
        return "Script run for '%s' on '%s'" % (str(self.script), str(self.started))


class ResultFile(Model):
    """An R script can output multiple files"""
    result = ForeignKey(ScriptResult, related_name='files')
    fn     = FileField('File', upload_to='rpy/out/')

    kind   = CharField(max_length=12, choices=(), null=True, blank=True)
    order  = IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        try:
            return self.fn.url
        except:
            return "BROKEN FILE"

    def read(self):
        self.fn.open('r')
        ret = self.fn.read()
        self.fn.close()
        return ret

    def media_type(self):
        ext= self.fn.name.rsplit('.', 1)[-1]
        if ext in ('png', 'svg'):
            return 'image'
        elif ext in ('csv',):
            return 'table'
        elif ext in ('txt', 'nfo',):
            return 'text'
        elif ext in ('html', 'xhtml', 'htm'):
            return 'html'
        elif ext in ('pdf','xls',):
            return 'file'
        return None


