from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.core.urlresolvers import reverse_lazy, reverse

from .models import *

class CategoryAdmin( admin.ModelAdmin ):
    fieldsets = [
        ( 'Name', {'fields': [ 'name' ] } ),
    ]
    list_display        = ( 'name', )

class EmailTemplateAdmin( admin.ModelAdmin ):
    fieldsets = [
        ( 'Email',          {'fields': [ 'category', 'txtid', 'subject', 'body', 'active' ] } ),
        ( 'Core',           {'fields': [ 'created', 'modified' ], 'classes': ['collapse closed'] } ),
    ]
    list_filter         = [ 'category' ]
    search_fields       = [ 'category', 'subject', 'body' ]
    list_display        = ( 'category', 'subject', 'txtid', 'active' )
    readonly_fields     = ( 'txtid', )


class EmailReceiptAdmin( admin.ModelAdmin ):

    def rendered_html(self, obj):
        
        return '<iframe src="%s" style="width: 745px; height: 600px" ></iframe>'%( obj.get_rendered_url() )
    rendered_html.allow_tags = True

    autocomplete_lookup_fields = {
        'fk': ('category',),
        'm2m': ()
    }
    raw_id_fields = ('category',)

    fieldsets = [
        ( 'Email',          
            {'fields': ( 
                ('email',),
                ('rendered_subject',),
                ('rendered_html'),
                'key',
                'category'  
            ),
            'classes': ( 'grp-collapse grp-open',) 
        } ),
        ( 'Stats',           
            {'fields': (
                ('viewed', 'view_count'),
                ('first_viewed_date', 'last_viewed_date'),
                ('created', 'modified')
            ),
            'classes': ( 'grp-collapse grp-open',)
        }),

        ( 'Errors',           
            {'fields': (
                ('sending_error'),  
                ('sending_error_message'),                
            ),
            'classes': ( 'grp-collapse grp-open',)
        }),
        ( 'Raw HTML',           
            {'fields': (
                ('rendered_body'),                
            ),
            'classes': ( 'grp-collapse grp-closed',)
        }),
    ]
    list_filter         = [ 'email', 'viewed' ]
    search_fields       = [ 'email', 'rendered_subject', 'rendered_body' ]
    list_display        = ( 'email', 'rendered_subject', 'viewed', 'view_count',
                            'created', 'sending_error', 'first_viewed_date', 
                            'last_viewed_date' )
    readonly_fields     = ( 'rendered_subject','rendered_body', 'key','email',
                            'viewed','view_count','first_viewed_date', 
                            'last_viewed_date', 'modified','created',
                            'rendered_html', 'sending_error', 
                            'sending_error_message', 'category')  
    csv_fields = flatten_fieldsets(fieldsets)  


class EmailSubscriptionCategoryAdmin( admin.ModelAdmin ):

    
    prepopulated_fields = {"txtid": ("title",)}

    core_fields = (        
        ('title','txtid'),
        'description',
        'can_be_viewed_online',
        'requires_explicit_opt_in',
        'can_unsubscribe',
        ('created')
    )
    fieldsets = (
        ("Category", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open', )
        }),
    )
    # csv_fields = flatten_fieldsets(fieldsets)  
    readonly_fields = ('created',)
    list_display = ('title', 'txtid', 'can_be_viewed_online', 
        'requires_explicit_opt_in','can_unsubscribe')
    list_filter = ('can_be_viewed_online','requires_explicit_opt_in',
        'can_unsubscribe')


class EmailCategorySubscriptionSettingsInline( admin.TabularInline ):
    model = EmailCategorySubscriptionSettings  
    fk_name = 'parent'

    autocomplete_lookup_fields = {
        'fk': ('category',),
        'm2m': ()
    }
    raw_id_fields = ('category',)

    fields = ('category','status')
    
    extra = 0

class UserSubscriptionSettingsAdmin( admin.ModelAdmin ):    

    fields = (
        'recipient_email',
        'key',
        'created'
    )
    # csv_fields = flatten_fieldsets(fieldsets)  
    list_display = ('recipient_email',)
    list_filter = ('recipient_email',)
    readonly_fields = ('created',)
    inlines = [EmailCategorySubscriptionSettingsInline]


admin.site.register( Category, CategoryAdmin )
admin.site.register( EmailTemplate, EmailTemplateAdmin )
admin.site.register( EmailReceipt, EmailReceiptAdmin )
admin.site.register( EmailSubscriptionCategory, EmailSubscriptionCategoryAdmin )
admin.site.register( UserSubscriptionSettings, UserSubscriptionSettingsAdmin )