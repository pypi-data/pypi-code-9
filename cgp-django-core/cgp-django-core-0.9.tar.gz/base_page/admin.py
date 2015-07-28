from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.contrib import messages

from .models import PageBase
from .forms import LinkItemForm

class BaseChildPageInline(admin.TabularInline):
    verbose_name = "Child"
    verbose_name_plural = "Children"

    fk_name = "parent"
    sortable_field_name = "order"
    extra = 0
    max_num = 0
    fieldsets = (
        ("", {
            'fields': (
                ('title', 'order', 'path',),
            )
        }),
    )
    readonly_fields = ('title', 'path', )

class BasePageAdmin(admin.ModelAdmin):

    def edit_parent_url(self, obj):
        if obj.pk:
            if obj.parent:
                object_type = type(obj.parent).__name__            
                url = reverse('admin:%s_%s_change' %(obj.parent._meta.app_label,  obj.parent._meta.model_name),  args=[obj.parent.id] )
                return u"<div style='min-width:278px'><a href='%s'>< Edit %s</a></div>"%(url, obj.parent.title)       
        return '<div style="min-width:278px"></div>'
    edit_parent_url.allow_tags = True

    actions = ["make_published", "make_wfr", "make_wip", "make_unpublished","reindex_items", "resave_item","retire_item",]
    autocomplete_lookup_fields = {
        'fk': ('parent',),
    }

    raw_id_fields = ('parent',)
    date_hierarchy = ("created")
    ordering = ("hierarchy",)
    prepopulated_fields = {"slug": ("title",)}

    list_display = ( 
        "admin_title", "path", "title", 'template_name',"redirect_path","state",
    )
    
    list_filter = (
        "parent", "state", "created_by", "modified_by", "template_name", 
        "redirect_path","authentication_required","display_in_sitemap",
        "sitemap_changefreq","sitemap_priority","robots_directive",
        "social_share_type"
    )
    search_fields = (
        "path", "slug", "title", "content", "synopsis", "sub_title", 
        "page_meta_description", "page_meta_keywords"
    )

    readonly_fields = (
        "admin_title", "modified_by", "created_by", "created", "modified", 
        "published","path", 'edit_parent_url'
    )

    


    core_fields = (
        ('edit_parent_url', 'parent',),
        ('title','slug'),        
        'sub_title',
        'state',
        ('template_name',),
        'synopsis',
        'content',
    )
   
    path_fields = (
        ('path', 'path_override'),
        ('redirect_page', 'redirect_path'),
        ('authentication_required'),
        'order'

    )

    seo_fields = (
        'page_meta_description',
        'page_meta_keywords',
        ('display_in_sitemap','sitemap_changefreq'),
        ('sitemap_priority', 'robots_directive'),
        'is_searchable',
        'is_shareable',
        'social_share_type',
        'social_share_title',
        'social_share_description',
        # 'social_share_image',
        'facebook_author_id',
        'twitter_author_id',
        'google_author_id'
    )


    meta_fields = (
        ('created_by', 'created'),
        ('modified_by', 'modified'),
        'published'
    )


    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open',)
        }),
        ("Page Path", {
            'fields': path_fields,
            'classes': ( 'grp-collapse grp-closed',)
        }),
        ("SEO", {
            'fields': seo_fields,
            'classes': ( 'grp-collapse grp-closed',)
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    csv_fields = flatten_fieldsets(fieldsets) 

    def reindex_items(self, request, queryset):
        if self.search_index:
            for item in queryset:
                self.search_index().update_object(item)
            messages.success(request, "%s items re-indexed"%(len(queryset)))
        else:
            messages.warning(request, "Search index class not specified")

    def retire_item(self, request, queryset):
        for page in queryset:
            page.retire(request)            
        messages.success(request, "%s items retired"%(len(queryset)))
    
    def resave_item(self, request, queryset):
        for page in queryset:
            page.save()
        messages.success(request, "%s items re-saved"%(len(queryset)))

    def reindex_item(self, request, queryset):
        for page in queryset:
            page.save()
        messages.success(request, "%s items re-saved"%(len(queryset)))
    
    def rebuild_path(self, request, queryset):
        for page in queryset:
            page.rebuild_path()            
        messages.success(request, "%s item paths rebuilt"%(len(queryset)))

    def make_published(self, request, queryset):
        for page in queryset:
            page.state = PageBase.PUBLISHED
            page.save()
        messages.success(request, "%s items Published"%(len(queryset)))
    make_published.short_description = "Mark selected items as Published"

    def make_wfr(self, request, queryset):
        queryset.update(state=PageBase.WFR)
        messages.success(request, "%s pages set to Waiting for Review"%(len(queryset)))
    make_wfr.short_description = "Mark selected items as Waiting For Review"

    def make_wip(self, request, queryset):
        queryset.update(state=PageBase.WIP)
        messages.success(request, "%s pages set to Work in Progess"%(len(queryset)))
    make_wip.short_description = "Mark selected items as Work in Progress"

    def make_unpublished(self, request, queryset):
        queryset.update(state=PageBase.UNPUBLISHED)
        messages.success(request, "%s pages Unpublished"%(len(queryset)))
    make_unpublished.short_description = "Mark selected items as Unpublished"

    def set_template_name(self, request, queryset):
        opts = self.model._meta
        app_label = opts.app_label
        if request.POST and request.POST.get("template_name"):
            queryset.update(template_name=request.POST.get("template_name"))
            return redirect('.')
        ctx = {
            'opts': opts,
            'app_label': app_label,
            'queryset': queryset
        }
        return render_to_response(
            template_name="admin/%s/set_template_name.html" % app_label,
            context_instance=RequestContext(request, ctx))
    set_template_name.short_description = "Set template name"

    

    def save_model(self, request, obj, form, change):
        if not getattr(obj, "created_by"):
            obj.created_by = request.user
        obj.modified_by = request.user
        super(BasePageAdmin, self). save_model(request, obj, form, change)



class BaseLinkItemInlines(admin.StackedInline):
    form = LinkItemForm
    
    def edit_children(self, obj):
        if obj.pk:
            object_type = type(obj).__name__            
            url = reverse('admin:%s_%s_change' %(obj._meta.app_label,  obj._meta.model_name),  args=[obj.id] )
            return u"<div style='min-width:278px'><a href='%s'>Edit child links ></a></div>"%(url)       
        return '<div style="min-width:278px"></div>'
    edit_children.allow_tags = True

    #model = LinkItem
    verbose_name = "Child Link"
    verbose_name_plural = "Child Links"

    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    
    extra = 0
    sortable_field_name = "order"
    
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }



    
    core_fields = (
        ('state','edit_children'),
        ('title',),
        ( 'content_type', 'object_id', 'path_override',)
    )
    extra_fields = (
        'url',
        ('order','target'),
        ('css_classes', 'extra_attributes'),        
    )

    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open',)
        }),
        ("Extra", {
            'fields': extra_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    readonly_fields = ('url','edit_children')    
    ordering = ('order',)

    


class BaseLinkItemAdmin(BasePageAdmin):
    form = LinkItemForm
    core_fields = (
        ('edit_parent_url','parent',),
        ('title','slug'),
        'path_override',
        ('content_type', 'object_id',),
        'path',
        'css_classes',
        'extra_attributes',
        'state'
    )
    meta_fields = (
        ('created_by', 'created'),
        ('modified_by', 'modified'),
        'published'
    )
    fieldsets = (
        ("Main Body", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open',)
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    csv_fields = flatten_fieldsets(fieldsets) 
    ordering = ('hierarchy',)
    
    list_display = ('admin_title', 'title', 'state','url',)
    list_display_links = ('title',)
    list_filter = ('parent',)

    readonly_fields = (
        "modified_by", "created_by", "created", "modified", "published","path", 
        'edit_parent_url', 
    )
    

    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
        'fk': ['parent',]
    }
    raw_id_fields = ('parent',)
    
    # inlines = [LinkItemInlines]

    # class Media:
    #     css = {
    #         "all": ('admin/css/wide_columns.css',)
    #     }



class BaseContentBlockAdmin(admin.ModelAdmin):

    prepopulated_fields = {"slug": ("title",)}

    list_display = ( 
        "title", "slug", "modified"
    )    
    search_fields = (
         "slug", "title", "content",
    )
    readonly_fields = (
        "modified_by", "created_by", "created", "modified", 
    )

    
    core_fields = (
        ('title','slug'),  
        'content',
    )
    meta_fields = (
        ('created_by', 'created'),
        ('modified_by', 'modified'),
        'published'
    )
    fieldsets = (
        ("Main", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open',)
        }),        
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )
    csv_fields = flatten_fieldsets(fieldsets) 

    

    def save_model(self, request, obj, form, change):
        if not getattr(obj, "created_by"):
            obj.created_by = request.user
        obj.modified_by = request.user
        super(BaseContentBlockAdmin, self). save_model(request, obj, form, change)

class BasePageContentBlockInline(admin.StackedInline):
    verbose_name = "Additional Content Blocks"
    verbose_name_plural = "Additional Content Blocks"

    fk_name = "parent"
    sortable_field_name = "order"
    extra = 0
    
    # classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    core_fields = (
        ('order','title',),
        ('content',),
        ( 'state','slug')
    )

    fieldsets = (
        ("Content", {
            'fields': core_fields
        }),
    )

    readonly_fields = ('slug', )
