import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
import django.dispatch
from django.db import models
from django.db.models import get_model
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .search_indexes import *



from monomail.utils import send_mail, send_monomail

from .utils import COUNTRIES, USPS_CHOICES, unique_slugify

from .manager import UserManager


NONE = ""
MR = "Mr."
MS = "Ms."
MRS = "Mrs."
DR = "Dr."
HONORIFICS = (
    (NONE, "None"),
    (MR, MR),
    (MS, MS),
    (MRS, MRS),
    (DR, DR),
)


BANNED = -20
BLOCKED = -10
NONE = 0
FLAGGED = 5
SUBMITTED = 10
APPROVED = 20
STATUS = (
    (BLOCKED, "Blocked"),
    (FLAGGED, "Flagged"),
    (NONE, "(None)"),
    (SUBMITTED, "Submitted"),
    (APPROVED, "Approved"),
)


"""
AbstractBaseUser: password, last_login, is_active
PermissionsMixin: is_superuser, groups, user_permissions
"""

class AbstractEmailUser(AbstractBaseUser, PermissionsMixin):
    """
    This is AbstractUser without the 'username' field
    """

    USERNAME_FIELD = "email"
   
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    class Meta:
        abstract = True

    def get_short_name(self):
        return self.email

    def get_full_name(self, include_honorific=False, include_designatory=False):
        if self.first_name and self.last_name:
            name = u"%s %s" % (self.first_name, self.last_name)
        else:
            name = self.email

        if include_honorific and self.honorific:
            name = "%s %s"%(self.honorific, name)

        if include_designatory and self.designatory:
            name = "%s, %s"%(name, self.designatory)

        return name

    @property
    def page_title(self):
        return self.get_full_name()

    def __unicode__(self):
        return self.get_full_name()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "last_name__icontains", "first_name__icontains", "email__icontains",)
    
    @property
    def username(self):
        """Hack to make Django Registration work w/o a username"""
        return self.email

    #EMAIL OVERRIDES:
    def email_user(self, subject, template, context={}):
        #TODO
        ctx = {'user': self}
        ctx = dict(ctx.items() + context.items())
        send_mail(self.email, subject, template, ctx)

    def send_activation_email(self, site):
        ctx_dict = {'activation_key': self.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'user':self}

        send_monomail(self.email, settings.EMAIL_ACCOUNT_REGISTRATION, ctx_dict)

    def send_registration_email(self, site):    

        ctx_dict = {'site': site,
                    'user':self}
        send_monomail(self.email, settings.EMAIL_ACCOUNT_CREATED, ctx_dict)

    def send_password_reset(self, ctx_dict):

        send_monomail(self.email, settings.EMAIL_PASSWORD_RESET, ctx_dict)

    def save(self, *args, **kwargs):

        #Clean names and email
        if self.first_name:
            self.first_name = self.first_name.strip()
        if self.last_name:
            self.last_name = self.last_name.strip()
        if self.email:
            self.email = self.email.strip().lower()

        super(AbstractEmailUser, self).save(*args, **kwargs)

    @property
    def edit_item_url(self):
        if self.pk:
            object_type = type(self).__name__
            url = reverse('admin:%s_%s_change' %(self._meta.app_label,  self._meta.model_name),  args=[self.id] )
            return url
        return None


class ContactMixin(models.Model):
    

    honorific = models.CharField(_('Honorific'), max_length=30, blank=True, choices=HONORIFICS)
    designatory = models.CharField(_('Designatory Letters'), max_length=30, blank=True, help_text="e.g. M.D. or CPA")#, choices=DESIGNATORIES)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True, help_text="YYYY-MM-DD")



    # -- Contact Info
    phone                   = models.CharField (_("Phone"),max_length=255, null = True, blank = True )
    address_1               = models.CharField(_("Address 1"), max_length=255,blank=True, null=True)
    address_2               = models.CharField(_("Address 2"), max_length=255,blank=True, null=True)
    city                    = models.CharField(_("City"), max_length = 50, null = True,  blank = True)
    state                   = models.CharField(_("State"), choices=USPS_CHOICES, max_length=255,blank=True, null=True)
    province                = models.CharField(_("Province"), max_length = 30, null = True, blank = True )
    country                 = models.CharField(_("Country"), choices=COUNTRIES, max_length=255,blank=True, null=True)
    zipcode                 = models.CharField(_("Zip"), max_length = 30, null = True, blank = True )

    def get_google_map_url(self):
        #This uses address only
        address = self.address_1.replace(' ', '+')
        city = self.city.replace(' ', '+')
        state = self.state if self.state else self.province
        country = '' if not self.country else self.country

        return 'https://www.google.com/maps/place/%s,+%s,+%s+%s+%s'%(address, city, state, country, self.zipcode)

    class Meta:
        abstract = True


class SocialMixin(models.Model):
    #NOTE settings.IMAGE_MODEL must point to the related image model
    avatar = models.ForeignKey(settings.IMAGE_MODEL, blank=True, help_text="Select a profile photo.",
        null=True, on_delete=models.SET_NULL) 

    avatar_status = models.IntegerField(default=NONE, choices=STATUS)

    # -- Social Media
    slug = models.CharField( _("URL Slug"), max_length = 255, 
        blank = True, null=True, unique = True, db_index=True)

    facebook_url = models.CharField(_("Facebook"), max_length=200, blank = True, 
        null = True, help_text=_('Please include http or https in the url.'))
    twitter_url = models.CharField(_("Twitter"), max_length=200, blank = True, 
        null = True, help_text=_('Please include http or https in the url.'))
    googleplus_url = models.CharField(_("Google+"), max_length=200, blank = True, 
        null = True, help_text=_('Please include http or https in the url.'))
    linkedin_url = models.CharField(_("Linkedin"), max_length=200, blank = True, 
        null = True, help_text=_('Please include http or https in the url.'))
    social_email = models.CharField(_("Social Email"), max_length=200, 
        blank = True, null = True)
    website = models.CharField(_("Website"), max_length=200, blank = True, 
        null = True)

    bio = models.TextField(blank=True, null=True)

    @property
    def has_social_media_url(self):
        return self.facebook_url or self.twitter_url or self.googleplus_url or self.linkedin_url or self.social_email or self.website

    def get_avatar(self):
        is_allowed = (self.avatar_status == APPROVED) or \
            (self.avatar_status == SUBMITTED and settings.AVATAR_REQUIRE_APPROVAL == False) or \
            (self.avatar_status == FLAGGED and (settings.AVATAR_HIDE_ON_FLAG == False or settings.AVATAR_REQUIRE_APPROVAL == False))
        if self.avatar and is_allowed:
            return self.avatar
        else:
            try:
                image_model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])
                return image_model.objects.get(pk=settings.AVATAR_DEFAULT_PK)
            except:
                return None

    def get_avatar_thumbnail_url(self):
        avatar = self.get_avatar()
        if avatar:
            return avatar.thumbnail_url
        return None              

    def flag_avatar(self, request=None):
        if not self.avatar or self.avatar_status == FLAGGED:
            return
            
        self.avatar_status = FLAGGED
        self.save()
        #if request:
        #    messages.success(request, 'User %s\'s avatar has been blocked.'%(self))

    def approve_avatar(self, request=None):
        if not self.avatar or self.avatar_status == APPROVED:
            return

        self.avatar_status = APPROVED
        BaseUserIndex().update_object(self)
        self.save()
        if request:
            messages.success(request, 'User %s\'s avatar has been approved.'%(self))

    def block_avatar(self, request=None):
        if not self.avatar or self.avatar_status == BLOCKED:
            return

        self.avatar_status = BLOCKED
        self.save()
        if request:
            messages.success(request, 'User %s\'s avatar has been blocked.'%(self))

    def ban_avatar(self, request=None):
        if not self.avatar or self.avatar_status == BANNED:
            return

        self.avatar_status = BANNED
        self.save()
        if request:
            messages.success(request, 'User %s has been banned from adding avatars.'%(self))

    def generate_slug(self):
        if self.first_name and self.last_name and not self.slug:
            raw_slug = u"%s %s"%(self.first_name, self.last_name)
            unique_slugify(self, raw_slug)

    def save(self, *args, **kwargs):


        #If avatar is changed, then set the avatar status to submitted
        avatar_changed = False
        if self.pk is not None and self.avatar:
            original = self._default_manager.get(pk=self.pk)
            if original.avatar != self.avatar:
                avatar_changed = True
        elif self.avatar:
            avatar_changed = True

        if avatar_changed and not self.avatar_status == BANNED:
            self.avatar_status = SUBMITTED            

        if not self.avatar:
            self.avatar_status = NONE

        if avatar_changed:
            user_avatar_change.send(sender=get_user_model(), user=self)


        #Generate slug
        self.generate_slug()        

        super(SocialMixin, self).save(*args, **kwargs)

    

    class Meta:
        abstract = True        


class BaseUserLink(models.Model):
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

    parent = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.PositiveIntegerField('order', null = True, blank=True)
    title = models.CharField(_('Title'), max_length=255, blank=True)
    
    target = models.CharField(_('Target'), max_length=255, 
        choices=TARGET_CHOICES, default=SELF)    
    css_classes = models.CharField(_('CSS Classes'), max_length=255, null=True, 
        blank=True)
    extra_attributes = models.CharField(_('Extra HTML Attributes'), 
        max_length=255, null=True, blank=True)
    
    class Meta:
        abstract = True   
        ordering = ['order',]


class UserLinkItem(BaseUserLink):
    #Model for additional custom links.   
    
    url = models.CharField(_("Website"), max_length=200, blank = True, 
        null = True)

    class Meta:
        abstract = True   

class SocialLink( UserLinkItem ):

    TYPE_EMAIL = 'email'
    TYPE_WEBSITE = 'website'
    TYPE_PHONE = 'phone'
    TYPE_TWITTER = 'twitter'
    TYPE_FACEBOOK = 'facebook'
    TYPE_GOOGLEPLUS = 'googleplus'
    TYPE_LINKEDIN = 'linkedin'
    TYPE_PINTEREST = 'pinterest'
    TYPE_TUMBLR = 'tumblr'
    TYPE_WORDPRESS = 'wordpress'
    
    SERVICE_TYPES = (
        (TYPE_EMAIL, "Email"),
        (TYPE_WEBSITE, "Website"),
        (TYPE_PHONE, "Phone Number"),
        (TYPE_TWITTER, "Twitter"),
        (TYPE_FACEBOOK, "Facebook"),
        (TYPE_GOOGLEPLUS, "Google Plus"),
        (TYPE_LINKEDIN, "LinkedIn"),
        (TYPE_PINTEREST, "Pinterest"),
        (TYPE_TUMBLR, "Tumblr"),
        (TYPE_WORDPRESS, "Wordpress")
    )

    type = models.CharField(_('Type'), max_length=255, 
        choices=SERVICE_TYPES, null=True, blank=True)    
    
    class Meta:
        abstract = True  


class UserPhoneNumbers( BaseUserLink ):

    phone_number = models.CharField(_('Phone Number'), max_length=255, blank=True)
    
    class Meta:
        abstract = True   

class UserEmailAddresses( BaseUserLink ):

    email_address = models.CharField(_('Email Address'), max_length=255, blank=True)
    
    class Meta:
        abstract = True         

       



class BaseUserGroup( models.Model ):
    
    help = {
        'title': "",
        'slug': "",
    }

    try:
        parent = models.ForeignKey(settings.AUTH_USER_GROUP_MODEL, blank=True, null=True)
    except:
        #not implemented
        pass
    order = models.PositiveSmallIntegerField(default=1)

    slug = models.CharField(_('Unique Text ID'), max_length=255, blank=True, 
        unique=True, db_index=True, help_text=help['slug'])

    title = models.CharField(_('Title'), max_length=255, help_text=help['title'])
    description = models.TextField(_('description'), blank=True)

    # -- Meta Data
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_created_by', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_modified_by', on_delete=models.SET_NULL)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)

    def get_edit_url(self):
        return reverse('admin:%s_%s_change' %(self._meta.app_label,  self._meta.model_name),  args=[self.id] )

    def get_members(self):
        user_member_model = get_model(settings.AUTH_USER_GROUP_MEMBER_MODEL.split('.')[0], settings.AUTH_USER_GROUP_MEMBER_MODEL.split('.')[1])
        return user_member_model.objects.filter(group=self).order_by('order')

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
        
        super(BaseUserGroup, self).save(*args, **kwargs)

    def __unicode__(self):
        # if self.parent:
        #     return '%s > %s'%(self.parent.__unicode__(), self.title)
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", "description__icontains")

    #Generated
    class Meta:
        abstract = True   
        ordering = ('-parent__slug', 'order',) 


class BaseUserGroupMember(models.Model):
    
    try:
        group = models.ForeignKey(settings.AUTH_USER_GROUP_MODEL)
    except:
        #not implemented
        pass
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.PositiveIntegerField('order', null = True, blank=True)
    
    class Meta:
        abstract = True   
        ordering = ['order',]    



class NotificationsMixin(models.Model):
    
    receive_notifications = models.BooleanField(_('Recieve Notifications'), 
        default=True, help_text=_('Recieve site notifications'))
    subscribed_to_newsletter = models.BooleanField(_('Subscribed to Newsletter'), 
        default=False)

    class Meta:
        abstract = True


    def save(self, *args, **kwargs):

        #If avatar is changed, then set the avatar status to submitted
        newsletter_subscription_change = False
        if self.pk is not None:
            original = self._default_manager.get(pk=self.pk)
            if original.subscribed_to_newsletter != self.subscribed_to_newsletter:
                newsletter_subscription_change = True
        else:
            newsletter_subscription_change = True

        if newsletter_subscription_change:
            user_newsletter_subscription_change.send(sender=get_user_model(), user=self)

        super(NotificationsMixin, self).save(*args, **kwargs)

class LocationMixin(models.Model):

    latitude = models.FloatField('latitude', blank=True, null=True)
    longitude = models.FloatField('longitude', blank=True, null=True)

    class Meta:
        abstract = True

    @property
    def lat(self):
        return self.latitude

    @property
    def lon(self):
        return self.longitude

    def get_google_map_url(self):
        #This uses lat and lon only
        return 'http://maps.google.com/maps?z=12&t=m&q=loc:%s+%s'%(self.lat, self.lon)
    
    def get_static_google_map_url(self):
        map_url = 'http://maps.googleapis.com/maps/api/staticmap?'
        map_url += 'center='
        map_url += str(self.lat) + ',' + str(self.lon)
        map_url += '&zoom=10'
        map_url += '&scale=2'
        map_url += '&size=860x300'
        map_url += '&maptype=roadmap'
        map_url += '&format=png'
        map_url += '&visual_refresh=true'
        map_url += '&markers=color:0x00b3e0%7Clabel:%7C'
        map_url += str(self.lat) + ',' + str(self.lon)
        map_url += '&style=feature:water%7Celement:geometry%7Ccolor:0xe9e9e9%7Clightness:17%7C'
        map_url += '&style=feature:landscape%7Celement:geometry%7Ccolor:0xf5f5f5%7Clightness:20%7C'
        map_url += '&style=feature:road.highway%7Celement:geometry.fill%7Ccolor:0xffffff%7Clightness:17%7C'
        map_url += '&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0xffffff%7Clightness:29%7Cweight:0.2%7C'
        map_url += '&style=feature:road.arterial%7Celement:geometry%7Ccolor:0xffffff%7Clightness:18%7C'
        map_url += '&style=feature:road.local%7Celement:geometry%7Ccolor:0xffffff%7Clightness:16%7C'
        map_url += '&style=feature:poi%7Celement:geometry%7Ccolor:0xf5f5f5%7Clightness:21%7C'
        map_url += '&style=feature:poi.park%7Celement:geometry%7Ccolor:0xdedede%7Clightness:21%7C'
        map_url += '&style=element:labels.text.stroke%7Cvisibility:on%7Ccolor:0xffffff%7Clightness:16%7C'
        map_url += '&style=element:labels.text.fill%7Csaturation:36%7Ccolor:0x333333%7Clightness:40%7C'
        map_url += '&style=element:labels.icon%7Cvisibility:off%7C'
        map_url += '&style=feature:transit%7Celement:geometry%7Ccolor:0xf2f2f2%7Clightness:19%7C'
        map_url += '&style=feature:administrative%7Celement:geometry.fill%7Ccolor:0xfefefe%7Clightness:20%7C'
        map_url += '&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0xfefefe%7Clightness:17%7Cweight:1.2%7C'
        return map_url


"""
class User(AbstractEmailUser, ContactMixin, SocialMixin, NotificationsMixin):
       

    # -- Managers
    objects = UserManager()
        

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "last_name__icontains", "first_name__icontains", "title__icontains", )


    def get_absolute_url(self):
        #TODO
        return None   

"""
    



# -----------------------------------------------------------------------------
# -- Signals
# -----------------------------------------------------------------------------
user_avatar_change = django.dispatch.Signal(providing_args=["user"])
user_newsletter_subscription_change = django.dispatch.Signal(providing_args=["user"])


# method for updating
def user_created_notification(sender, instance, **kwargs):
    created = kwargs['created']

    try:

        #don't notify for selenium tests
        try:
            test_user = settings.TEST_USER
        except:
            test_user = None

        
        if (test_user and instance.email != test_user) or not test_user:
            ctx_dict = {'site': Site.objects.get_current(), 'user':instance}
            if created:
                user_model = get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
                admins = user_model.objects.filter(groups__name=settings.REGISTRATION_NOTIFICATION_GROUP)
                for admin in admins:
                    send_monomail(admin.email, settings.EMAIL_USER_ACCOUNT_CREATED, ctx_dict)

    except:
        #unable to send registration notifications
        pass


    try:
        if created and settings.ACCOUNT_SEND_REGISTRATION_EMAIL:
            current_site = Site.objects.get_current()
            instance.send_registration_email(current_site)
    except:
        #unable to send user registration email
        pass



# register the signal
try:
    #pre 1.7
    user_model = get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])
    post_save.connect(user_created_notification, sender=user_model, dispatch_uid="user_created_notification")
except:
    post_save.connect(user_created_notification, sender=settings.AUTH_USER_MODEL, dispatch_uid="user_created_notification")






