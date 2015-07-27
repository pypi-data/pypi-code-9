from django.db import models
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now
from django.utils.safestring import mark_safe

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from .manager import PageManager
from .utils import get_page_templates, unique_slugify


def get_default_template():        
    try:
        default_template = settings.PAGES_DEFAULT_TEMPLATE
    except:
        default_template = "pages/default.html"

    return default_template

def get_templates():        

    default_template = get_default_template()

    try:
        template_dir = settings.PAGES_TEMPLATE_DIR
    except:
        template_dir = 'pages/'

    try:ignore_templates = settings.PAGES_IGNORE_TEMPLATES
    except:
        ignore_templates = ('pages/base.html',)

    templates = get_page_templates(default_template, template_dir, ignore_templates)
    return templates


class PathMixin(models.Model):
    """
    Path Mixin
    ==========

    The Path Mixin provides the Pages app with the ability to nest pages and
    build a URL consisting of the parent and slug fields.
    """

    help = {
        'parent': 'The parent this item will be nested under.',
        'path': "The URL path to this item, defined by the parent path and the text id or by path_override.",
        'hierarchy': "The hierarchy of this item, defined by the parent path, the order and the text id.",
        'path_override': "Explicitly set the items's path using the format: /my/custom/path/",
        'redirect_page': "Permanently redirect item",
        'redirect_path': "Path to redirect to.",
    }

    parent = models.ForeignKey('self', blank=True, null=True,
        related_name="children", help_text=help['parent'], on_delete=models.SET_NULL)

    path = models.CharField(_('path'), max_length=255, unique=True,
        help_text=help['path'])
    hierarchy = models.CharField(_('hierarchy'), max_length=255, unique=True,
        null=True, blank=True, help_text=help['hierarchy'])

    path_override = models.CharField(_('path override'), max_length=255,
        blank=True, help_text=help['path_override'])

    redirect_page = models.BooleanField(default=False, 
        help_text=help['redirect_page'])
    redirect_path = models.CharField(_('Redirect Path'), max_length=255,
        blank=True, help_text=help['redirect_path'])

    class Meta:
        abstract = True

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)

    @property
    def parent_slug(self):
        if self.parent:
            return self.parent.slug
        return None

    @property
    def parent_pk(self):
        if self.parent:
            return self.parent.id
        return None

    @property
    def parent_title(self):
        if self.parent:
            return self.parent.title
        return None

    def get_path(self):
        if self.path_override:
            return self.path_override
        return self.path

    def _build_path(self):
        if self.path_override:
            return self.path_override
        elif self.parent:
            return "%s%s/" % (self.parent.path, self.slug)
        else:
            return "/%s/" % self.slug

    def _build_raw_path(self):
        if self.parent:
            return "%s%s/%s/" % (self.parent._build_raw_path(), str(self.order).zfill(3), self.slug)
        else:
            return "/%s/" % self.slug

    def get_pagetree(self):
        def _get_parent_obj(page, tree):
            if page.parent:
                tree.append(page.parent)
                _get_parent_obj(page.parent, tree)
        tree = [self]
        _get_parent_obj(self, tree)
        tree.reverse()
        return tree
        

    def update_path(self):
        # print "update path %s"%(self)
        previous_path = self.path if self.pk else None
        self.path = self._build_path()
        self.hierarchy = self._build_raw_path()
        
    def update_children(self):
        [p.save() for p in self.get_children()]


    def save(self, *args, **kwargs):  

        #Dont let link item point to self
        if self.parent and self.parent == self:
            self.parent = None

        super(PathMixin, self).save(*args, **kwargs)




class SEOMixin(models.Model):
    """
    SEO Mixin
    =========

    Fields to support old HTML Meta SEO fields description and keywords.
    """
    help = {
        'page_meta_description': "A short description of the page, used for SEO and not displayed to the user.",
        'page_meta_keywords': "A short list of keywords of the page, used for SEO and not displayed to the user.",
        'is_shareable': "Show sharing widget",
        'social_share_title': "The page title used when the page is shared on social networks.",
        'social_share_description': "A description of the page used with the page is shared on social networks.",
        'social_share_image': "Standards for the social share image vary, but an image at least 300x200px should work well.",
        'facebook_author_id': "Numeric Facebook ID",
        'twitter_author_id': "Twitter handle, including \"@\" e.g. @cgpartners",
        'google_author_id': "Google author id, e.g. the AUTHOR_ID in https://plus.google.com/AUTHOR_ID/posts",
        'display_in_sitemap': "If object should be displayed in the sitemap",
        'sitemap_priority': "Enter a number between 0 and 1.0",
        'sitemap_changefreq': "How frequently the page is likely to change.",
        'robots_directive': "Robots index/noindex and follow/nofollow directives",
        'is_searchable': "Item appears in internal site search."
    }

    page_meta_description = models.CharField(_('Meta Description'), 
        max_length=2000, blank=True, help_text=help['page_meta_description'])
    page_meta_keywords = models.CharField(_('Meta Page Keywords'), 
        max_length=2000, blank=True, help_text=help['page_meta_keywords'])


    #Sitemap Settings:
    CHANGE_ALWAYS = 'always'
    CHANGE_HOURLY = 'hourly'
    CHANGE_DAILY = 'daily'
    CHANGE_WEEKLY = 'weekly'
    CHANGE_MONTHLY = 'monthly'
    CHANGE_YEARLY = 'yearly'
    CHANGE_NEVER = 'never'   

    CHANGEFREQ_CHOICES = (
        (CHANGE_ALWAYS, "Always"),
        (CHANGE_HOURLY, "Hourly"),
        (CHANGE_DAILY, "Daily"),
        (CHANGE_WEEKLY, "Weekly"),
        (CHANGE_MONTHLY, "Monthly"),
        (CHANGE_YEARLY, "Yearly"),
        (CHANGE_NEVER, "Never")        
    )

    ROBOTS_INDEX_FOLLOW     = 'INDEX, FOLLOW'
    ROBOTS_NOINDEX_FOLLOW   = 'NOINDEX, FOLLOW'
    ROBOTS_INDEX_NOFOLLOW   = 'INDEX, NOFOLLOW'
    ROBOTS_NOINDEX_NOFOLLOW = 'NOINDEX, NOFOLLOW'

    ROBOTS_CHOICES = (
        (ROBOTS_INDEX_FOLLOW, ROBOTS_INDEX_FOLLOW),
        (ROBOTS_NOINDEX_FOLLOW, ROBOTS_NOINDEX_FOLLOW),
        (ROBOTS_INDEX_NOFOLLOW, ROBOTS_INDEX_NOFOLLOW),
        (ROBOTS_NOINDEX_NOFOLLOW, ROBOTS_NOINDEX_NOFOLLOW), 
    )
    
    display_in_sitemap = models.BooleanField(default=True,
        help_text=help['display_in_sitemap'])
    sitemap_priority = models.CharField("Sitemap Priority", max_length=255, 
        null=True, blank=True, default='0.5', help_text=help['sitemap_priority'])
    sitemap_changefreq = models.CharField("Sitemap Change Frequency", 
        max_length=255, null=True, blank=True, choices=CHANGEFREQ_CHOICES, 
        default=CHANGE_NEVER, help_text=help['sitemap_changefreq'],  )
    robots_directive = models.CharField("Robots Index and Follow Directive", 
        max_length=255, choices=ROBOTS_CHOICES, default=ROBOTS_INDEX_FOLLOW, 
        help_text=help['robots_directive'] )
    is_searchable = models.BooleanField( _("Is Searchable"), default = True,
        help_text=help['is_searchable'])



    #OG Type Choices
    MUSIC_SONG = 'music.song'
    MUSIC_ALBUM = 'music.album'
    MUSIC_PLAYLIST = 'music.playlist'
    MUSIC_RADIO = 'music.radio_station'
    VIDEO_MOVIE = 'video.movie'
    VIDEO_EPISODE = 'video.episode'
    VIDEO_TV_SHOW = 'video.tv_show'
    VIDEO_OTHER = 'video.other'
    ARTICLE = 'article'
    BOOK = 'book'
    PROFILE = 'profile'
    WEBSITE = 'website'  
    BLOG = 'blog'
    TYPE_CHOICES = (
        (ARTICLE, "Article"),
        (BOOK, "Book"),
        (PROFILE, "Profile"),
        (WEBSITE, "Website"),
        (BLOG, "Blog"),
        (VIDEO_MOVIE, "Video - Movie"),
        (VIDEO_EPISODE, "Video - Episode"),
        (VIDEO_TV_SHOW, "Video - TV Show"),
        (VIDEO_OTHER, "Video - Other"),
        (MUSIC_SONG, "Music - Song"),
        (MUSIC_ALBUM, "Music - Album"),
        (MUSIC_PLAYLIST, "Music - Playlist"),
        (MUSIC_RADIO, "Music - Radio Station"),
    )

    is_shareable = models.BooleanField( _("Is Shareable"), 
        default = False,help_text=help['is_shareable'] )
    social_share_title = models.CharField("Social title", max_length=255, 
        null=True, blank=True, help_text=help['social_share_title'])
    social_share_type = models.CharField("Social type", max_length=255, 
        null=True, blank=True, choices=TYPE_CHOICES, default=ARTICLE )
    social_share_description = models.CharField("Social description", 
        max_length=255, null=True, blank=True, 
        help_text = help['social_share_description'])
    social_share_image = models.ImageField(_("Preferred Social Share Image"),
        upload_to="page/social_share_image/", null=True, blank=True,
        help_text=help['social_share_image'])

    facebook_author_id = models.CharField("Facebook Author ID", 
        max_length=255, null=True, blank=True, 
        help_text=help['facebook_author_id'])
    twitter_author_id = models.CharField("Twitter Admin ID", max_length=255, 
        null=True, blank=True, help_text=help['twitter_author_id'])
    google_author_id = models.CharField("Google Admin ID", max_length=255, 
        null=True, blank=True, help_text=help['google_author_id'])

    class Meta:
        abstract = True

    @property
    def page_title(self):
        if self.social_share_title:
            return self.social_share_title
        return self.title

    def save(self, *args, **kwargs):
  

        if not self.sitemap_priority and hasattr(self, 'default_sitemap_priority') and self.default_sitemap_priority:
            print 'item doesnt have sitemap priority, but it does have default: %s'%(self.default_sitemap_priority)
            self.sitemap_priority = self.default_sitemap_priority

        if not self.sitemap_changefreq and hasattr(self, 'default_sitemap_changefreq') and self.default_sitemap_changefreq:
            print 'item doesnt have sitemap changefrreq, but it does have default: %s'%(self.default_sitemap_changefreq)
            self.sitemap_changefreq = self.default_sitemap_changefreq

        super(SEOMixin, self).save(*args, **kwargs)


class PageBase(models.Model):

    # -- Choice Data
    UNPUBLISHED = 5
    WIP = 10
    WFR = 15
    PUBLISHED = 20

    STATE_CHOICES = (
        (WIP, "Work in Progress"),
        (WFR, "Waiting for Review"),
        (PUBLISHED, "Published"),
        (UNPUBLISHED, "Unpublished")
    )

    NONE = 0
    REGISTERED_USER = 10
    ADMIN = 100
    AUTHENTICATION_CHOICES = (
        (NONE, "None"),
        (REGISTERED_USER, "Registered User"),
        (ADMIN, "Admin")
    )

    # -- Help Text Strings
    help = {
        'title': "",
        'slug': "Auto-generated text id. WARNING: Changing \
        this will change the URL of this page, potentially breaking anything \
        that links to it. Be sure to create a URL redirect to the old URL using\
         in the LegacyURL section.",
        'sub_title': "A caption / sub-title / headline, or other one-sentence \
        description of the page.",
        'synopsis': "Synoposis or preview text."
    }
    
    AUTO_SAVE_CHILDREN_ON_PATH_UPDATE = False
    CHANGE_PATH_ON_SLUG_CHANGE = False

    

    slug = models.CharField(_('Unique Text ID'), max_length=255, blank=True, 
        db_index=True, help_text=help['slug'])

    title = models.CharField(_('Title'), max_length=255, 
        help_text=help['title'])
    sub_title = models.CharField(_('Sub Title'), max_length=2000, blank=True,
        help_text=help['sub_title'])

    try:
        max_synopsis_length = settings.MAX_SYNOPSIS_LENGTH
    except:
        max_synopsis_length = 250        
    synopsis = models.TextField(_('Synopsis'), blank=True, null=True,
        help_text=help['synopsis'], max_length=max_synopsis_length, )

    # -- Page Content
    template_name = models.CharField(_('Template Name'), max_length=255, 
        default=get_default_template(), choices=get_templates())
    content = models.TextField(_('Page Content'), blank=True)

    # -- State    
    state = models.IntegerField(choices=STATE_CHOICES, default=WIP)
    authentication_required = models.IntegerField(choices=AUTHENTICATION_CHOICES, 
        default=NONE)
    order = models.PositiveSmallIntegerField(default=1)

    # -- Meta Data
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_created_by', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_modified_by', on_delete=models.SET_NULL)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    published = models.DateTimeField(_('Published Date'), blank=True, 
        null=True)

    objects = PageManager()

    class Meta:
        abstract = True
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ('parent__slug', 'order',)
        permissions = (
            ("can_publish", "Can Publish"),
        )

    def __unicode__(self):
        return "%s [%s]" % (self.title, self.path)

    def get_absolute_url(self):
        return reverse("pages_page", args=[], kwargs={"path": self.get_path()[1:]})
    
    def get_children(self):
        return self.__class__.objects.filter(parent=self)

    def get_published_children(self):
        return self.__class__.objects.published().filter(parent=self)

    @property
    def page_title(self):
        return self.title

    @property
    def admin_levels(self):
        if self.parent:
            return "%s<span style='color:#fff'>|------</span>" % self.parent.admin_levels
        else:
            return ""

    @property
    def admin_title(self):
        if self.parent:
            return mark_safe("%s&lfloor; %s" % (self.admin_levels, self.title))
        else:
            return self.title

    def get_templates():
        return get_page_templates()

    def retire(self, request=None):

        #1 -- set page to unpublished
        self.state = self.UNPUBLISHED
        self.redirect_page = True
        self.save()

        #2 -- Set up a redirect for this page
        path = self.get_absolute_url()
        if path.startswith("/"):
            path = path[1:]

        try:
            #If user has legacy url installed, use that
            from site_admin.models import LegacyURL
            redirect = LegacyURL.create_legacy_url(path, self.title, referer_url=None, referer_title=None)
            edit_url = reverse('admin:%s_%s_change' %(redirect._meta.app_label,  redirect._meta.model_name),  args=[redirect.id] )
        except:
           redirect = None

        
        if redirect:
            messages.success(request, u'IMPORTANT: Please specify the redirect path for %s - %s at %s'%(self.pk, self.title, edit_url))
        else:
            messages.success(request, u'IMPORTANT: Please specify the redirect path for %s - %s'%(self.pk, self.title))


    def save(self, *args, **kwargs):

        if self.pk:
            original = self.__class__.objects.get(pk=self.pk)
        else:
            original = None

        # -- Make sure slug is unique
        if self.slug and self.slug != '':
            unique_slugify(self, self.slug)
        elif self.title and self.title != '':
            unique_slugify(self, self.title)  
        else:
            unique_slugify(self, "Untitled %s"%(self.__class__.__name__))    

        # -- Always lowercase slug:
        if self.slug:
            self.slug = self.slug.lower()
        
        # -- Update published date
        is_newly_published = (original!=None) and (original.state != self.PUBLISHED) and (self.state == self.PUBLISHED)
        is_new_and_published = self.state == self.PUBLISHED and not self.published
        if is_newly_published or is_new_and_published:
            self.published = now()



        # -- Update path
        slug_changed = (original!=None) and (original.slug != self.slug)
        path_override_changed = (original!=None) and (original.path_override != self.path_override)
        parent_changed = (original!=None) and (original.parent != self.parent)

        url_changed = ((not self.path or not self.hierarchy) or \
            ( self.CHANGE_PATH_ON_SLUG_CHANGE and slug_changed) or \
            ( self.CHANGE_PATH_ON_SLUG_CHANGE and parent_changed) or\
            ( self.CHANGE_PATH_ON_SLUG_CHANGE and path_override_changed))


        if url_changed:
            self.update_path()

        

        super(PageBase, self).save(*args, **kwargs)

        if url_changed and self.AUTO_SAVE_CHILDREN_ON_PATH_UPDATE:
            for child in self.get_children():
                child.update_path()
                child.save()

        
class BasePageContentBlock( models.Model ):
    
    help = {
        'title': "",
        'slug': "Auto-generated text id for this content block. This will be the variable name used in the template for this block.",
    }

    # Implement in actual class:
    # parent = models.ForeignKey('Page')
    
    slug = models.CharField(_('Unique Text ID'), max_length=255, blank=True, 
        help_text=help['slug'])

    title = models.CharField(_('Title'), max_length=255, help_text=help['title'], null=True, blank=True)
    content = models.TextField(_('Content'), null=True, blank=True)

    order = models.PositiveIntegerField(default = 0, blank=True, null=True, db_index=True)

    state = models.IntegerField(choices=PageBase.STATE_CHOICES, default=PageBase.PUBLISHED)
        # -- Meta Data
    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    published = models.DateTimeField(_('Published Date'), blank=True, 
        null=True)

    def get_siblings(self, published=True):
        if published:
            return self.__class__.objects.filter(parent=self.parent).filter(state=PageBase.PUBLISHED)
        else:
            return self.__class__.objects.filter(parent=self.parent)


    def save(self, *args, **kwargs):

        slug_base = 'page_block_'
        siblings = self.get_siblings()
        # -- Make sure slug is unique
        if self.slug:
            raw_slug = self.slug
        elif self.title:
            raw_slug = "%s%s"%(slug_base,self.title)
        else:
            parent_child_count = len(siblings)+1
            raw_slug = "%s%s"%(slug_base, parent_child_count)

        raw_slug = raw_slug.lower()
        
        unique_slugify(self, raw_slug, 'slug', siblings, "_")

        
        super(BasePageContentBlock, self).save(*args, **kwargs)

    def get_title(self):
        if self.title:
            return "Page Blog %s"%(self.title)
        return "Page Blog %s"%(self.slug)

    @property
    def page_title(self):
        return self.title

    def __unicode__(self):
        return self.get_title()

    #Generated
    class Meta:
        ordering = [ 'order']
        abstract = True   


class LinkItem( PageBase, PathMixin ):
    
    help = {
        'url': 'Generated link url',
        'css_classes': 'Extra CSS classes to add to the link item',
        'extra_attributes': "Extra attributes to add to the link item",
        'content_type': "Choose an object in the CMS to dynamically point to",
        'target':"Should link open in the same window (_self) or a new one (_blank)?"
    }

    BLANK = '_blank'
    SELF = '_self'
    PARENT = '_parent'
    TOP = '_top'
    TARGET_CHOICES = (
        (BLANK, _(BLANK)),
        (SELF, _(SELF)),
        (PARENT, _(PARENT)),
        (TOP, _(TOP))        
    )

    #RELATED TO OBJECT
    try:
        content_type = models.ForeignKey(ContentType, blank = True, null=True, 
            on_delete=models.SET_NULL, help_text=help['content_type'],
            limit_choices_to={"model__in": settings.LINK_ITEM_MODEL_CHOICES})      
    except:
        content_type = models.ForeignKey(ContentType, blank = True, null=True, 
            help_text=help['content_type'], on_delete=models.SET_NULL)

    object_id = models.PositiveIntegerField(blank = True, null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    url = models.CharField(_("URL"), max_length = 255, blank = True,
        help_text=help['url'])

    target = models.CharField(_('Target'), max_length=255, 
        help_text=help['target'], choices=TARGET_CHOICES, default=SELF)
    
    css_classes = models.CharField(_('CSS Classes'), max_length=255, null=True, 
        blank=True, help_text=help['css_classes'])
    extra_attributes = models.CharField(_('Extra HTML Attributes'), 
        max_length=255, null=True, blank=True, help_text=help['extra_attributes'])

    #Generated
    class Meta:
        abstract = True
        ordering = [ 'order']
        verbose_name = "Link Item"
        verbose_name_plural = "Link Items"


    def __unicode__(self):
        return self.title


    def _build_path(self):
        if self.path_override:
            return self.path_override
        else:
            if self.content_object:
                return self.content_object.get_absolute_url()
            else:
                return ''

    def update_path(self):
        previous_path = self.path if self.pk else None
        self.path = self.slug
        self.url = self._build_path()
        self.hierarchy = self._build_raw_path()

    def html(self):
        return '<a href="%s" %s %s %s>%s</a>'%(self.url, self.get_target(), self.get_classes(), self.get_attributes(), self.title)
    
    def get_attributes(self):
        if self.extra_attributes:
            return self.extra_attributes
        return ''

    def get_classes(self):
        if self.css_classes:
            return 'class="%s"'%(self.css_classes)
        return ''
        
    def get_target(self):
        if self.path:    
            if 'http' in self.path:
                return 'target=_blank'
            else:
                return ''
        else:
            return ''

    def save(self):
        self.update_path()

        if not self.title:
            print 'set title...'
            try:
                self.title = self.content_object.title
            except:
                pass

        super(LinkItem, self).save()



class BaseContentBlock( models.Model ):
    
    help = {
        'title': "",
        'slug': "Auto-generated text id for this content block.",
    }

    slug = models.CharField(_('Unique Text ID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])

    title = models.CharField(_('Title'), max_length=255, help_text=help['title'])
    content = models.TextField(_('Content'), blank=True)

    # -- Meta Data
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_created_by', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_modified_by', on_delete=models.SET_NULL)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)
    published = models.DateTimeField(_('Published Date'), blank=True, 
        null=True)

    @property
    def page_title(self):
        return self.title

    def save(self, *args, **kwargs):

        # -- Make sure slug is unique
        if self.slug and self.slug != '':
            unique_slugify(self, self.slug)
        elif self.title and self.title != '':
            unique_slugify(self, self.title)  
        else:
            unique_slugify(self, "Untitled %s"%(self.__class__.__name__))    

        # -- Always lowercase slug:
        if self.slug:
            self.slug = self.slug.lower()
        
        super(BaseContentBlock, self).save(*args, **kwargs)

    #Generated
    class Meta:
        abstract = True    