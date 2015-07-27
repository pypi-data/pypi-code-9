from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.auth.admin import UserAdmin as ContribUserAdmin
from django.contrib.admin.util import flatten_fieldsets
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from django.contrib.auth.models import Group

from .forms import *
from .search_indexes import *
from .models import APPROVED
from monomail.utils import send_mail_template, get_email_template

class GroupListFilter(SimpleListFilter):
    title = 'group'
    parameter_name = 'group'
    def lookups(self, request, model_admin):
        groups = Group.objects.all()
        items = ()
        for group in groups:
            items += ((str(group.id), str(group.name),),)
        return items

    def queryset(self, request, queryset):
        group_id = request.GET.get(self.parameter_name, None)
        if group_id:
            return queryset.filter(groups=group_id)
        return queryset

class BaseUserAdmin(ContribUserAdmin):

    def send_email(self, request, queryset):        

        if request.POST.get('post'):

            subject = request.REQUEST.get('subject')
            body = request.REQUEST.get('body')
            notifications = request.REQUEST.get('notifications')
            

            count = 0
            site =  Site.objects.get_current()
            for user in queryset:
                receives_notifications = (user.receive_notifications and notifications) or (not notifications)

                if receives_notifications:
                    ctx_dict = {'site': site, 'user':user}
                    send_mail_template(user.email, subject, body, ctx_dict)
                    count += 1

            messages.success(request, u'%s users emailed'%(count))
            return HttpResponseRedirect(request.get_full_path())

        else:

            template = get_email_template(settings.EMAIL_USER_TEMPLATE)
            
            return render_to_response('admin/send_email.html', 
            {
                'queryset': queryset, 
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                'template':template
            }, 
            context_instance=RequestContext(request))
    send_email.short_description = "Send users an email"

    def set_default_password(self, request, queryset):
        for object in queryset:
            object.set_password(settings.DEFAULT_PASSWORD)
            object.save()
            messages.success(request, "Password reset for %s (%s)"%(object.get_full_name(),object.email))
            
    set_default_password.short_description = "Set password to default (%s)"%(settings.DEFAULT_PASSWORD)

    def reindex_items(self, request, queryset):
        for item in queryset:
            BaseUserIndex().update_object(item)
        messages.success(request, '%s items reindexed.'%(len(queryset)))

    def impersonate_user(self, obj):
        return "<a target='_blank' href='/?__impersonate=%s'>Impersonate</a>"%(obj.pk)
    impersonate_user.allow_tags = True

    def approve_user_avatars(self, request, queryset):
        for item in queryset:
            item.approve_avatar(request)
        messages.success(request, '%s user avatars have been approved'%(len(queryset)))

    def block_user_avatars(self, request, queryset):
        for item in queryset:
            item.block_avatar(request)
        messages.success(request, '%s user avatars have been block'%(len(queryset)))

    def ban_user_avatars(self, request, queryset):
        for item in queryset:
            item.block_avatar(request)
        messages.success(request, '%s users have been banned from using avatars'%(len(queryset)))

    
    def avatar_thumbnail(self, obj):
        try:
            if obj.avatar and obj.avatar_status != APPROVED and settings.AVATAR_REQUIRE_APPROVAL:
                return "<img src='%s' style='width:50px;'/><br /><br />Submitted:<br /><br /><img src='%s' style='width:50px;'/>"%(obj.get_avatar().thumbnail_url, obj.avatar.thumbnail_url)
            else:
                return "<img src='%s' style='width:50px;'/>"%(obj.get_avatar().thumbnail_url)
        except:
            return ""
    avatar_thumbnail.allow_tags = True


    autocomplete_lookup_fields = {
        'fk': ['avatar',],
    }
    raw_id_fields = ('avatar', )
    filter_horizontal = ('groups',)


    user_fields = (
        ('first_name','last_name'),
        'email',
        'password',
    )
    permission_fields = (
        'is_active',
        'is_staff',
        'is_superuser',
        'groups',
        ('date_joined', 'last_login')
    )
    contact_fields = (
        ('honorific', 'designatory'),
        ('title',),
        ('date_of_birth', 'phone'),
        ('address_1',),
        ('address_2',),
        ('city',),
        ('state',),
        ('province',),
        ('country'),
        ('zipcode'),
    )
    social_fields = (
        ('avatar_thumbnail', 'avatar','avatar_status'),
        'slug',
        'facebook_url',
        'twitter_url',
        'linkedin_url',
        'googleplus_url',
        'social_email',
        'website',
        'bio'
    )
    notification_fields = (
        'receive_notifications',
        'subscribed_to_newsletter'
    )
    fieldsets = (
        ('Name', { 
            'fields': user_fields
        }),

        ('Contact Info', { 
            'fields': contact_fields
        }),
        ('Social Links', { 
            'fields': social_fields
        }),
        (_('Permissions'), {
            'fields': permission_fields
        }),
        (_('Notification Settings'), {
            'fields': notification_fields
        }),
    )
    form = AccountUserChangeForm
    add_form = AccountUserCreationForm
    add_fieldsets = (
        ("User", {
            'classes': (),
            'fields': ('email', 'password1', 'password2','first_name','last_name',)}
        ),
    )    
    readonly_fields = ('last_login','date_joined', 'impersonate_user', 
        'avatar_thumbnail')    
    list_display = (
        'avatar_thumbnail', 'email','last_name','first_name', 
        'date_joined', 'last_login','impersonate_user'
    )
    list_display_links = ('avatar_thumbnail', 'email','last_name', 
        'first_name')
    ordering = ('last_name','first_name',)

    list_filter = ('is_active', 'is_superuser','is_staff', GroupListFilter,
        'avatar_status',  'receive_notifications', 'subscribed_to_newsletter')
    search_fields = ('first_name', 'last_name', 'email', 'title')
    csv_fields = flatten_fieldsets(fieldsets) 
    actions = ('set_default_password','reindex_items', 'send_email', 
        'approve_user_avatars', 'block_user_avatars', 'ban_user_avatars')


class BaseUserMemberInline(admin.TabularInline):
    verbose_name = "Member"
    verbose_name_plural = "Members"

    autocomplete_lookup_fields = {
        'fk': ['user',],
    }
    raw_id_fields = ('user', )

    fk_name = "group"
    sortable_field_name = "order"
    extra = 0
    fieldsets = (
        ("", {
            'fields': (
                ( 'order','user',),
            )
        }),
    )

class BaseChildGroupInline(admin.TabularInline):
    verbose_name = "Child"
    verbose_name_plural = "Children"

    def edit_url(self, obj):
        url = obj.get_edit_url()
        return '<a href="%s">Edit %s &gt;</a>'%(url, obj.title)
    edit_url.allow_tags = True

    fk_name = "parent"
    sortable_field_name = "order"
    extra = 0
    max_num = 0
    fieldsets = (
        ("", {
            'fields': (
                ( 'order','title', 'edit_url'),
            )
        }),
    )
    readonly_fields = ('title', 'edit_url')

class BaseUserGroupAdmin(admin.ModelAdmin):
    
    def edit_parent_url(self, obj):
        if obj.parent:
            return '<a href="%s">Edit parent &gt;</a>'%(obj.parent.get_edit_url())
        return ''
    edit_parent_url.allow_tags = True
    
    list_filter = ('parent',)
    list_display = ('parent','title')
    list_display_links = ('title',)

    core_fields = (
        ('parent', 'edit_parent_url'),
        ('title','slug'),
        'description'
    )
    meta_fields = (
        ('created_by', 'created'),
        ('modified_by', 'modified')
    )
    fieldsets = (
        ("Core", {
            'fields': core_fields,
            'classes': ( 'grp-collapse grp-open',)
        }),
        ("Meta", {
            'fields': meta_fields,
            'classes': ( 'grp-collapse grp-closed', )
        })
    )

    readonly_fields = ('created','modified', 'edit_parent_url')   

    autocomplete_lookup_fields = {
        'fk': ('parent',),
    }
    raw_id_fields = ('parent',)
    prepopulated_fields = {"slug": ("title",)}

    csv_fields = flatten_fieldsets(fieldsets) 

    # inlines = [BaseChildGroupInline]


    