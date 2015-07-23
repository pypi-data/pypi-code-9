from django.contrib.admin import *
from django.utils.safestring import mark_safe
from django_object_actions import DjangoObjectActions

from .models import *
from .forms import LibraryForm, ScriptWriter

def schedule_reinstall(modeladmin, request, queryset):
    queryset.update(installed=None, scheduled=True, attempted=None)
schedule_reinstall.short_description = "Re-schedule installation or upgrade"

class LibraryAdmin(ModelAdmin):
    list_display = ('__str__', 'is_installed', 'location', 'installed', 'scheduled', 'attempted')
    ordering = 'installed',
    actions = [ schedule_reinstall ]
    readonly_fields = ['installed', 'location', 'attempted', 'version']
    form = LibraryForm

class ResultsInline(TabularInline):
    fields = ['render_url', 'run_ok', 'started', 'ended', 'output', 'result']
    readonly_fields = ['render_url', 'run_ok', 'output', 'result', 'started', 'ended']
    model = ScriptResult
    extra = 0
    max_num = 0

    def render_url(self, obj):
        if obj.files.count() > 0:
            return mark_safe('<br/>'.join(
                '<a href="%s">%s</a>' % (r.fn.url, r.fn.name) \
                for r in obj.files.all()
            ))
        return "No Files"

    def run_ok(self, obj):
        return not obj.error
    run_ok.boolean = True


class FilesInline(TabularInline):
    files = ['fn', 'kind', 'order']
    model = ResultFile
    extra = 0


class UploadAdmin(DjangoObjectActions, ModelAdmin):
    form = ScriptWriter
    filter_horizontal = ('libs',)
    inlines = [ ResultsInline ]
    exclude = ['slug']
    readonly_fields = []
    objectactions = ('run', 'download')

    class Media:
        css = { 'all' : ('css/no-inline-label.css',) }

    def run(self, request, obj):
        obj.run()

    run.label = "Run Script"
    run.short_description = "Run this script right now (no save)"

    def download(self, request, obj):
        obj.run(save_instead=True)

    download.label = "Download Script"
    download.short_description = "Compile the script as it would be sent to R and output as the result instead of running."


class ResultAdmin(ModelAdmin):
    inlines = [ FilesInline ]


site.register(AvailableLibrary, LibraryAdmin)
site.register(UploadedModule)
site.register(UploadedScript, UploadAdmin)
site.register(ScriptResult, ResultAdmin)

