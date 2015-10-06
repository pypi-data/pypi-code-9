from gipsy.sections.forms_base import SectionAdminFormBase, SectionInlineAdminFormBase
from gipsy.sections.models import Section


class SectionAdminForm(SectionAdminFormBase):

    class Meta:
        model = Section
        fields = '__all__'


class SectionInlineAdminForm(SectionInlineAdminFormBase):

    class Meta:
        model = Section
        fields = '__all__'
