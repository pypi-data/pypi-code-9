from django.db.models import AutoField
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import DecimalField
from django.db.models import ForeignKey
from django.db.models import Model
from django.db.models import PositiveIntegerField
from django.db.models import PositiveSmallIntegerField
from django.db.models import TimeField

from localization.models import LocalizableObjectBase
from localization.models import LocalizableValueBase


class ContactType(LocalizableObjectBase):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Contact Type'
        verbose_name_plural = 'Contact Types'


class ContactTypeName(LocalizableValueBase):
    localizable_object  = ForeignKey(ContactType,                  blank=False, unique=False, related_name='names')


class OrganizationType(LocalizableObjectBase):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    is_published        = BooleanField(                            blank=False, unique=False, default=False, verbose_name='Is Published')

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Organization Type'
        verbose_name_plural = 'Organization Types'


class OrganizationTypeName(LocalizableValueBase):
    localizable_object  = ForeignKey(OrganizationType,             blank=False, unique=False, related_name='names')


class Organization(LocalizableObjectBase):
    id                  = PositiveIntegerField(                    blank=False, unique=True,  primary_key=True)
    country             = ForeignKey('locations.Country',          blank=False, unique=False, related_name='+')
    region              = ForeignKey('locations.Region',           blank=False, unique=False, related_name='+')
    type                = ForeignKey(OrganizationType,             blank=False, unique=False, related_name='+')
    code                = CharField(                               blank=False, unique=True,  max_length=64)
    is_published        = BooleanField(                            blank=False, unique=False, default=False)

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def get_code(self, code):
        try:
            return OrganizationCode.objects.get(organization=self, code=code).value.strip()
        except OrganizationCode.DoesNotExist:
            return ''

    def get_contact(self, code):
        try:
            return OrganizationContact.objects.get(organization=self, type__code=code).value.strip()
        except OrganizationContact.DoesNotExist:
            return ''

    @property
    def swift(self):
        return self.get_code('SWIFT')

    @property
    def iban(self):
        return self.get_code('IBAN')

    def __str__(self):
        return self.name

    class Meta:
        index_together      = [('type', 'id', ), ('country', 'id', ), ('region', 'id', )]
        verbose_name        = 'Organization'
        verbose_name_plural = 'Organizations'


class OrganizationName(LocalizableValueBase):
    localizable_object  = ForeignKey(Organization,                 blank=False, unique=False, related_name='names')


class OrganizationCode(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    organization        = ForeignKey(Organization,                 blank=False, unique=False, related_name='codes')
    code                = CharField(                               blank=False, unique=False, max_length=64)
    value               = CharField(                               blank=False, unique=False, max_length=64)

    def __str__(self):
        return self.value

    class Meta:
        index_together      = [('organization', 'code', 'value', 'id', )]
        unique_together     = [('organization', 'code', )]
        verbose_name        = 'Organization Code'
        verbose_name_plural = 'Organization Codes'


class OrganizationContact(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    organization        = ForeignKey(Organization,                 blank=False, unique=False, related_name='+')
    type                = ForeignKey(ContactType,                  blank=False, unique=False, related_name='+')
    value               = CharField(                               blank=False, unique=False, max_length=256)

    def __str__(self):
        return self.value

    class Meta:
        index_together      = [('organization', 'type', 'value', 'id', )]
        unique_together     = [('organization', 'type', )]
        verbose_name        = 'Organization Contact'
        verbose_name_plural = 'Organization Contacts'


class Branch(LocalizableObjectBase):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    organization        = ForeignKey(Organization,                 blank=False, unique=False, related_name='+')
    region              = ForeignKey('locations.Region',           blank=False, unique=False, null=True, related_name='+')
    code                = CharField(                               blank=False, unique=False, max_length=64)
    latitude            = DecimalField(                            blank=False, unique=False, max_digits=8, decimal_places=4)
    longitude           = DecimalField(                            blank=False, unique=False, max_digits=8, decimal_places=4)
    is_published        = BooleanField(                            blank=False, unique=False, default=False)

    def _get_name(self):
        return self._get_localizable_value(self.names, 'name', '')

    def _set_name(self, value):
        self._set_localizable_value(self.names, 'name', value)

    def _del_name(self,):
        self._del_localizable_value(self.names, 'name')

    name = property(_get_name, _set_name, _del_name)

    def _get_address(self):
        return self._get_localizable_value(self.addresses, 'address', '')

    def _set_address(self, value):
        self._set_localizable_value(self.addresses, 'address', value)

    def _del_address(self,):
        self._del_localizable_value(self.addresses, 'address')

    address = property(_get_address, _set_address, _del_address)

    def get_code(self, code):
        try:
            return BranchCode.objects.get(branch=self, code=code).value.strip()
        except BranchCode.DoesNotExist:
            return ''

    def get_contact(self, code):
        try:
            return BranchContact.objects.get(branch=self, type__code=code).value.strip()
        except BranchContact.DoesNotExist:
            return ''

    def __str__(self):
        return '{0}, {1}'.format(self.organization.name, self.name)

    class Meta:
        unique_together     = [('organization', 'code')]
        verbose_name        = 'Branch'
        verbose_name_plural = 'Branches'


class BranchName(LocalizableValueBase):
    localizable_object  = ForeignKey(Branch,                       blank=False, unique=False, related_name='names')


class BranchAddress(LocalizableValueBase):
    localizable_object  = ForeignKey(Branch,                       blank=False, unique=False, related_name='addresses')


class BranchCode(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    branch              = ForeignKey(Branch,                       blank=False, unique=False, related_name='+')
    code                = CharField(                               blank=False, unique=False, max_length=64)
    value               = CharField(                               blank=False, unique=False, max_length=64)

    def __str__(self):
        return self.value

    class Meta:
        index_together      = [('branch', 'code', 'value', 'id', )]
        unique_together     = [('branch', 'code')]
        verbose_name        = 'Branch Code'
        verbose_name_plural = 'Branch Codes'


class BranchContact(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    branch              = ForeignKey(Branch,                       blank=False, unique=False, related_name='+')
    type                = ForeignKey(ContactType,                  blank=False, unique=False, related_name='+')
    value               = CharField(                               blank=False, unique=False, max_length=256)

    def __str__(self):
        return self.value

    class Meta:
        index_together      = [('branch', 'type', 'value', 'id', )]
        unique_together     = [('branch', 'type', )]
        verbose_name        = 'Branch Contact'
        verbose_name_plural = 'Branch Contacts'


class BranchSchedule(Model):
    id                  = AutoField(                               blank=False, unique=True,  primary_key=True)
    branch              = ForeignKey(Branch,                       blank=False, unique=False, related_name='+')
    day_from            = PositiveSmallIntegerField(               blank=False, unique=False)
    day_till            = PositiveSmallIntegerField(               blank=False, unique=False)
    time_from           = TimeField(                               blank=False, unique=False)
    time_till           = TimeField(                               blank=False, unique=False)

    def __str__(self):
        return "%s - %s" % (self.time_from, self.time_till)

    class Meta:
        index_together      = [('branch', 'day_from', 'time_from', 'time_from', 'time_till', 'id', )]
        unique_together     = [('branch', 'day_from', 'time_from', )]
        verbose_name        = 'Branch Schedule'
        verbose_name_plural = 'Branch Schedules'
