from django.contrib.admin import ModelAdmin
from django.contrib.admin.sites import site

from token_auth.models import Token


class TokenAdmin(ModelAdmin):
    fieldsets = [
        ('Identity', {'classes': ('wide', ), 'fields': [('code')]}),
        ('Value',    {'classes': ('wide', ), 'fields': [('user', ), ('method_pattern',), ('path_pattern', )]}),
        ('Period',   {'classes': ('wide', ), 'fields': [('valid_from',), ('valid_till', )]}),
        ('Hashes',   {'classes': ('wide', ), 'fields': [('can_md5', 'can_sha1', ), ('can_sha256', 'can_sha512', )]}),
        ('Secret',   {'classes': ('wide', ), 'fields': [('secret_text',)]}),
    ]
    list_display    = ['code', 'user', 'path_pattern', 'method_pattern']
    readonly_fields = ['secret_text']
    list_editable   = []
    list_filter     = []
    ordering        = ['user', 'path_pattern', 'method_pattern']

    def secret_text(self, obj):
        return bytes(obj.secret).decode('ascii')


site.register(Token, TokenAdmin)
