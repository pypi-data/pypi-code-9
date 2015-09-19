from django.contrib.admin import ModelAdmin
from django.contrib.admin import TabularInline
from django.contrib.admin.sites import site

from deferred.models import Task
from deferred.models import Failure


class FailureInline(TabularInline):
    model = Failure
    extra = 0
    readonly_fields = ('exception_type', 'exception_args', )


class TaskAdmin(ModelAdmin):
    inlines = [
        FailureInline,
    ]
    fieldsets = [
        ('Contents',   {'classes': ('wide', ), 'fields': [('type', 'priority', )]}),
        ('Timestamps', {'classes': ('wide', ), 'fields': [('created_at', 'updated_at', )]}),
        ('Status',     {'classes': ('wide', ), 'fields': [('is_processed', 'is_succeeded', 'retry_count', )]}),
        ('Data',       {'classes': ('wide', ), 'fields': [('data_text', )]}),
    ]
    readonly_fields = ('type', 'priority', 'created_at', 'updated_at', 'is_succeeded', 'is_succeeded', 'retry_count', 'data_text', )
    list_display    = ['type', 'priority', 'created_at', 'updated_at', 'is_processed', 'is_succeeded', 'retry_count']
    list_editable   = []
    list_filter     = ['type', 'priority', 'created_at', 'updated_at', 'is_processed', 'is_succeeded', 'retry_count']
    ordering        = ['created_at']

    def data_text(self, obj):
        def escape(b):
            if (b >= 0x20) and (b <= 0x7F):
                return chr(b)
            elif b <= 0xFF:
                return r'\x{0:02x}'.format(b)
            elif b <= 0xFFFF:
                return r'\u{0:04x}'.format(b)
            else:
                return r'\U{0:08x}'.format(b)

        return ''.join(escape(b) for b in obj.data.tobytes())


site.register(Task, TaskAdmin)
