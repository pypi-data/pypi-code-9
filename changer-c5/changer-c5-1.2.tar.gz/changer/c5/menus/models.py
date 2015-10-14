from django import forms
from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from django.contrib import admin
from django.db import models
from django.db.models.signals import post_save, m2m_changed
from django.template.defaultfilters import slugify

LINK_CHOICES = (('flatpage', 'Flatpage'),('link', 'Link'))

class Menu(models.Model):
    title = models.CharField(max_length=50)
    parent_menu = models.ForeignKey("self", blank=True, null=True, related_name="children")
    is_main_menu = models.BooleanField()
    
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        super(Menu, self).save(*args, **kwargs)
        for link in self.link_set.all():
            link.save()
        
class Link(models.Model):
    link_type = models.CharField(max_length="10", choices=LINK_CHOICES)
    title = models.CharField(max_length=50, blank=True)
    flatpages = models.ManyToManyField('flatpages.FlatPage', verbose_name="Flatpage", blank=True, null=True)
    url = models.CharField(max_length=200, blank=True)
    active = models.BooleanField(default=True)
    menu = models.ForeignKey(Menu, blank=True, null=True)
    position = models.PositiveSmallIntegerField()
    
    class Meta:
        ordering = ['position']
    
    def __unicode__(self):
        if self.link_type == 'flatpage':
            try:
                return "Flatpage - %s" % (self.flatpages.all()[0].title)
            except:
                return "Flatpage - Empty"
        else:
            return "General - %s" % (self.url)
        
class LinkAdminForm(forms.ModelForm):
    class Meta:
        model = Link
        widgets = {
            'link_type': forms.RadioSelect(attrs={'class':'flatpage_menu_radio'}),
        }

class LinkAdminInline(admin.StackedInline):
    form = LinkAdminForm
    model = Link
    extra = 0
    radio_fields = {"link_type": admin.VERTICAL}
    raw_id_fields = ('flatpages',)  
    classes = ('collapse open',)
    sortable_field_name = "position"
    fieldsets = (
        (None, {
            'fields': ('title', 'flatpages', 'url', 'position', 'menu', 'active')
        }),
        ('Advanced options', {
            'fields': ('link_type',)
        }),)


class MenuAdmin(admin.ModelAdmin):
    inlines = [LinkAdminInline]
    list_display = ['title','is_main_menu']
    
    class Media:
        js = ("/layout/js/flatpage_menu.js",)
    
admin.site.register(Menu, MenuAdmin)

def link_save_handler(link, flatpage):
    """ Syncs flatpage with link """
    if link.url != flatpage.url or link.title != flatpage.title:
        link.url, link.title = flatpage.url, flatpage.title
        link.save()
    
def link_saved_callback(sender, **kwargs):
    """ Updates links to reflect related flatpage values """
    instance = kwargs['instance']
    if instance.flatpages.count():
        flatpage = instance.flatpages.all()[0]
        link_save_handler(instance, flatpage)
            
def flatpage_saved_callback(sender, **kwargs):
    """ Updates menu links urls when flatpage changes """
    instance = kwargs['instance']
    related_links = instance.link_set.all()
    for link in related_links:
        link_save_handler(link, instance)

post_save.connect(flatpage_saved_callback, sender=FlatPage)
m2m_changed.connect(link_saved_callback, sender=Link.flatpages.through)