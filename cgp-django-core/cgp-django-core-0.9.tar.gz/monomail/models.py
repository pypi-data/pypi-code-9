import uuid
from datetime import datetime
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

class Category( models.Model ):
    """
    Category
    ========
    Categories for Email Templates
    """
    
    name = models.CharField( max_length = 150, null = True )

    def __unicode__( self ):
        return self.name

    class Meta:
        verbose_name        = 'Email Template Category'
        verbose_name_plural = 'Email Template Categories'
        ordering            = [ 'name' ]

class EmailTemplate( models.Model ):
    """
    Email Template
    ==============
    Model for an email template.
    """
    
    category    = models.ForeignKey( Category, null = True, blank = True )
    txtid       = models.CharField( max_length = 200, blank = True, help_text = "" )
    
    subject     = models.CharField( max_length = 255, null = True )
    body        = models.TextField()
    
    active      = models.BooleanField( default = True )
    created     = models.DateTimeField( blank = True )
    modified    = models.DateTimeField( blank = True )
    
    @property
    def rendered( self ):
        return self.body
    
    def __unicode__( self ):
        return self.subject
    
    class Meta:
        verbose_name        = 'Email Template'
        verbose_name_plural = 'Email Templates'
        ordering            = [ 'category', 'subject' ]
        
    def save(self, *args, **kwargs):
        
        # -- Set Text ID
        if not self.txtid:
            self.txtid = slugify( self.subject )
            
        # -- Set Created
        if not self.created:
            self.created = datetime.now()
            
        self.modified = datetime.now()
        
        super( EmailTemplate, self ).save(*args, **kwargs)

class EmailReceipt(models.Model):
    email = models.CharField(_("Recipient"), max_length = 255, blank = False)
    rendered_subject = models.CharField(_("Rendered Subject"), max_length = 255, blank = False)
    rendered_body =  models.TextField(_('Rendered Body'), blank=True, null=True)
    
    key = models.CharField(_("key"), max_length=50, blank=True, null=True, unique=True)

    viewed = models.BooleanField(default=False,)
    view_count = models.PositiveIntegerField('View Count', default=0, null = True, blank=True)

    first_viewed_date = models.DateTimeField ( _("First Viewed Date"), blank=True, null=True )
    last_viewed_date = models.DateTimeField ( _("Last Viewed Date"), blank=True, null=True )

    created = models.DateTimeField ( _("Time created"), auto_now_add = True )
    modified = models.DateTimeField ( _("Time modified"), auto_now = True )
    
    category = models.ForeignKey('monomail.EmailSubscriptionCategory', null=True, blank=True)

    sending_error = models.BooleanField(default=False,)
    sending_error_message = models.TextField(blank=True, null=True)

    
    def save(self, *args, **kwargs):

        if not self.key:
            self.key = uuid.uuid1().hex  

        super(EmailReceipt, self).save(*args, **kwargs)      


    
    def get_absolute_url(self):
        return reverse('record_email_view', kwargs = {'key': self.key }) 

    def get_rendered_url(self):
        return reverse('email_rendered_view', kwargs = {'key': self.key }) 

    def get_online_url(self):
        return reverse('email_online_view', kwargs = {'key': self.key }) 


    @property
    def page_title(self):
        return self.rendered_subject 
        

    def record_view(self):
        if not self.first_viewed_date:
            self.first_viewed_date = datetime.now()
        
        self.last_viewed_date = datetime.now()

        self.view_count += 1
        self.viewed = True

        self.save()

    def record_error(self, messsage):
        self.sending_error = True
        self.sending_error_message = messsage
        self.save()

    def rendered(self, subject, message):
        self.rendered_subject = subject
        self.rendered_body = message
        self.save()

    def render_counter(self):
        site = Site.objects.get_current()        
        protocol = 'https' if settings.MONOMAIL['use_ssl'] else 'http'
        return '<img src="%s://%s%s" alt="Email Counter" style="width:1px;height:1px;" />'%(protocol, site.domain, self.get_absolute_url())

    @staticmethod
    def create_receipt(email, category=None):
        item = EmailReceipt( email=email, category=category )
        item.save()
        return item

    class Meta:
        verbose_name_plural = 'Email Receipts'

class EmailSubscriptionCategory(models.Model):
    help = {
        'can_be_viewed_online':"Allow recipients to view this online. DO NOT ENABLE if you are sending any kind of private data in this email category.",
        'requires_explicit_opt_in':"Sending these emails require user to explicitely opt-in to category.",
        'can_unsubscribe': "If these emails are transactional, then subscribe/unsubscribe functionality is not needed",
        # 'can_change_frequency': "If these emails be received at a different freququency",
    }

    created = models.DateTimeField ( _("Time created"), auto_now_add = True )
    title   = models.CharField(_("Title"), max_length = 255, null=True, blank=True)
    txtid   = models.CharField( max_length = 200, blank = True, help_text = "" )
    description = models.TextField(null=True, blank=True)

    can_be_viewed_online        = models.BooleanField(default=False, help_text=help['can_be_viewed_online'])
    requires_explicit_opt_in    = models.BooleanField(default=False, help_text=help['requires_explicit_opt_in'])
    can_unsubscribe             = models.BooleanField(default=True, help_text=help['can_unsubscribe'])
    # can_change_frequency      = models.BooleanField(default=True, help_text=help['can_change_frequency'])
    

    def save(self, *args, **kwargs):
        
        # -- Set Text ID
        if not self.txtid:
            self.txtid = slugify( self.title )
            
        
        super( EmailSubscriptionCategory, self ).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'Email Subscription Categories'

    def __unicode__( self ):
        return self.title

class UserSubscriptionSettings(models.Model):
    
    created = models.DateTimeField ( _("Time created"), auto_now_add = True )

    key = models.CharField(_("key"), max_length=50, blank=True, null=True, unique=True)
    
    recipient_email = models.CharField(_("Recipient Email"), max_length = 255)

    def get_absolute_url(self):
        try:
            return reverse('email_settings_view', kwargs = {'key': self.key })
        except:
            return None

    def get_settings(self, category=None):
        
        if category:

            category_settings, created = EmailCategorySubscriptionSettings.objects.get_or_create(parent=self,category=category)
            return category_settings
            
        else:
            return EmailCategorySubscriptionSettings.objects.filter(parent=self)

    def save(self, *args, **kwargs):

        if not self.key:
            self.key = uuid.uuid1().hex  

        super(UserSubscriptionSettings, self).save(*args, **kwargs)


    class Meta:
        verbose_name_plural = 'User subscription settings'

class EmailCategorySubscriptionSettings(models.Model):

    DEFAULT = 'default'
    UNSUBSCRIBED = 'unsubscribed'
    SUBSCRIBED = 'subscribed'
    NOTIFICATION_STATUS_CHOICES = (
        (DEFAULT, _("Default")),
        (UNSUBSCRIBED, _("Unsubscribed")),
        (SUBSCRIBED, _("Subscribed")),
    )

    created = models.DateTimeField ( _("Time created"), auto_now_add = True )
    
    parent = models.ForeignKey('monomail.UserSubscriptionSettings')

    category = models.ForeignKey('monomail.EmailSubscriptionCategory')
    
    status = models.CharField(choices=NOTIFICATION_STATUS_CHOICES, 
        default=DEFAULT, max_length = 255)
    
    def can_email(self):
        if self.category.requires_explicit_opt_in:
            if self.status != EmailCategorySubscriptionSettings.SUBSCRIBED:
                return False
        elif self.category.can_unsubscribe:
            if self.status == EmailCategorySubscriptionSettings.UNSUBSCRIBED:
                return False

        
        #WE MADE IT!
        return True

    class Meta:
        verbose_name_plural = 'Email Category subscription settings'

    def __unicode__( self ):
        return "%s:%s"%(self.category.title, self.status)

def get_settings_for_user(recipient_email, category=None):
    notification_settings_model = get_model_by_label(settings.EMAIL_SUBSCRIPTION_MODEL)
    notification_settings, created = notification_settings_model.objects.get_or_create(recipient_email=recipient_email)

    return notification_settings

def get_category_settings_for_user(recipient_email, category=None):
    notification_settings_model = get_model_by_label(settings.EMAIL_SUBSCRIPTION_MODEL)
    notification_settings, created = notification_settings_model.objects.get_or_create(recipient_email=recipient_email)

    if category:
        return notification_settings.get_settings(category)
    else:
        return notification_settings.get_settings()            

