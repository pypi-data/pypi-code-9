from django.db.models import AutoField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DateTimeField
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import Model
from django.db.models import PositiveIntegerField
from django.db.models import TextField
from django.db.models import URLField


class PropertyManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Property(Model):
    objects = PropertyManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    name                = CharField(                               blank=False, unique=True,  max_length=256)

    def natural_key(self):
        return (self.code, )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering            = ['name']
        index_together      = [('code', 'id')]
        unique_together     = [('name',)]
        verbose_name        = 'Property'
        verbose_name_plural = 'Properties'


class TemplateManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Template(Model):
    objects = TemplateManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    name                = CharField(                               blank=False, unique=True,  max_length=256)
    path                = CharField(                               blank=False, unique=True,  max_length=256)

    def natural_key(self):
        return (self.code, )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering            = ['name']
        index_together      = [('code', 'path', 'id')]
        unique_together     = []
        verbose_name        = 'Template'
        verbose_name_plural = 'Templates'


class PageManager(Manager):
    def get_path_from_parts(self, *path_parts):
        return '/'.join(path_parts)

    def get_parts_from_path(self, path):
        return path.split('/')

    def get_by_natural_key(self, *path_parts):
        return self.get(path=self.get_path_from_parts(*path_parts))


class Page(Model):
    objects = PageManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    path                = CharField(                               blank=True,  unique=False, null=True, max_length=256)
    url                 = URLField(                                blank=True,  unique=False, null=True, max_length=256)
    template            = ForeignKey(Template,                     blank=True,  unique=False, null=True, related_name='+')
    is_published        = BooleanField(                            blank=False, unique=False, default=False)

    def natural_key(self):
        return Page.objects.get_parts_from_path(self.path)

    def __str__(self):
        return self.path

    def load_properties(self, language_id):
        properties = {}

        for pageproperty in self.pageproperties.all():
            if pageproperty.language_id is None:
                properties[pageproperty.property.code] = pageproperty.value

        for pageproperty in self.pageproperties.all():
            if pageproperty.language_id == language_id:
                properties[pageproperty.property.code] = pageproperty.value

        self.properties = properties

    class Meta:
        ordering            = ['path']
        index_together      = []
        unique_together     = [('path',)]
        verbose_name        = 'Page'
        verbose_name_plural = 'Pages'


class HeaderManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Header(Model):
    objects = HeaderManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    name                = CharField(                               blank=False, unique=True,  max_length=256)
    contents            = TextField(                               blank=True,  unique=False)

    def natural_key(self):
        return (self.code, )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering            = ['name']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Header'
        verbose_name_plural = 'Headers'


class FooterManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Footer(Model):
    objects = FooterManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    name                = CharField(                               blank=False, unique=True,  max_length=64)
    contents            = TextField(                               blank=True,  unique=False)

    def natural_key(self):
        return (self.code, )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        ordering            = ['name']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Footer'
        verbose_name_plural = 'Footers'


class PageHeader(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    page                = ForeignKey(Page,                         blank=False, unique=False, null=True, related_name='headers')
    language            = ForeignKey('localization.Language',      blank=False, unique=False, null=True, related_name='+')
    header              = ForeignKey(Header,                       blank=True,  unique=False, null=True, related_name='+')

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.page, self.language, self.header)

    class Meta:
        ordering            = ['language']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Page Header'
        verbose_name_plural = 'Page Header'


class PageFooter(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    page                = ForeignKey(Page,                         blank=False, unique=False, null=True, related_name='footers')
    language            = ForeignKey('localization.Language',      blank=False, unique=False, null=True, related_name='+')
    footer              = ForeignKey(Footer,                       blank=True,  unique=False, null=True, related_name='+')

    def __str__(self):
        return '{0}-{1}-{2}'.format(self.page, self.language, self.footer)

    class Meta:
        ordering            = ['language']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Page Footer'
        verbose_name_plural = 'Page Footer'


class PageContents(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    page                = ForeignKey(Page,                         blank=False, unique=False, null=True, related_name='contents')
    language            = ForeignKey('localization.Language',      blank=False, unique=False, null=True, related_name='+')
    timestamp           = DateTimeField(                           blank=False, unique=False, auto_now=True)
    contents            = TextField(                               blank=True,  unique=False)

    def __str__(self):
        return '{0}-{1}'.format(self.page, self.language)

    class Meta:
        ordering            = ['language']
        index_together      = []
        unique_together     = [('page', 'language')]
        verbose_name        = 'Page Contents'
        verbose_name_plural = 'Page Contents'


class PageProperty(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    page                = ForeignKey(Page,                         blank=False, unique=False, null=True, related_name='pageproperties')
    property            = ForeignKey(Property,                     blank=False, unique=False, null=True, related_name='pageproperties')
    language            = ForeignKey('localization.Language',      blank=True,  unique=False, null=True, related_name='+')
    value               = CharField(                               blank=True,  unique=False, max_length=256)

    def __str__(self):
        return '{0}-{1}'.format(self.page, self.property)

    class Meta:
        ordering            = ['page']
        index_together      = [('page', 'property', 'language', 'value')]
        unique_together     = [('page', 'property', 'language')]
        verbose_name        = 'Page Property'
        verbose_name_plural = 'Page Properties'


class MenuManager(Manager):
    def get_by_natural_key(self, code):
        return self.get(code=code)


class Menu(Model):
    objects = MenuManager()

    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=False, max_length=64)
    name                = CharField(                               blank=False, unique=False, max_length=256)

    def natural_key(self):
        return (self.code, )

    def __str__(self):
        return self.name

    class Meta:
        ordering            = ['name']
        index_together      = []
        unique_together     = []
        verbose_name        = 'Menu'
        verbose_name_plural = 'Menus'


class MenuPage(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    menu                = ForeignKey(Menu,                         blank=False, unique=False, null=True, related_name='+')
    page                = ForeignKey(Page,                         blank=False, unique=False, null=True, related_name='+')
    order               = PositiveIntegerField(                    blank=False, unique=False)

    def __str__(self):
        return '{0}-{1}'.format(self.menu, self.page)

    class Meta:
        ordering            = ['order']
        index_together      = [('menu', 'order', 'page')]
        unique_together     = [('menu', 'page')]
        verbose_name        = 'Menu Page'
        verbose_name_plural = 'Menu Pages'
