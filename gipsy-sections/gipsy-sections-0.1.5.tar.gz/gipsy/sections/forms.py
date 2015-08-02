from gipsy.sections.forms_base import SectionAdminFormBase
from gipsy.sections.models import Section


class SectionAdminForm(SectionAdminFormBase):

    class Meta:
        model = Section
        fields = '__all__'
