from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField
from versatileimagefield.fields import VersatileImageField, PPOIField


class ContentBase(models.Model):
    """A base model for shared attributes/logic across stacks_page models."""

    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


@python_2_unicode_compatible
class ContentGroup(ContentBase):
    """A group of Content instances."""
    name = models.CharField(
        _('Name'),
        max_length=120,
        help_text="The internal name/signifier of this content."
    )
    display_title = models.CharField(
        _('Title'),
        max_length=120,
        help_text='The displayed-to-the-user title of this Content Group.',
        blank=True
    )

    class Meta:
        verbose_name = _('Content Group')
        verbose_name_plural = _('Content Groups')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Content(ContentBase):
    """Represents a block of content."""

    order = models.PositiveIntegerField(
        _('Order'),
        default=1
    )
    group = models.ForeignKey(
        ContentGroup,
        verbose_name=_('Content Group'),
        related_name='content_set'
    )
    title = models.CharField(
        _('Title'),
        max_length=120,
        help_text='The displayed-to-the-user title of this content.'
    )
    menu_image = VersatileImageField(
        _('Menu Image'),
        upload_to="content-group/",
        ppoi_field="menu_image_ppoi",
        help_text=_("The menu image for this content.")
    )
    alternate_menu_image = VersatileImageField(
        _('Alternate Menu Image'),
        upload_to="content-group/alternate_image",
        ppoi_field="alternate_menu_image_ppoi",
        help_text=_(
            "An optional alternate menu image used for 'hover' "
            "and 'open' states."
        ),
        blank=True
    )
    menu_image_ppoi = PPOIField()
    alternate_menu_image_ppoi = PPOIField()
    content = TextPlusStuffField(
        _('Content'),
        blank=True,
        null=True,
        help_text=_('The content of this section.')
    )

    class Meta:
        verbose_name = _('Content')
        verbose_name_plural = _('Content')
        ordering = ['order']

    def __str__(self):
        return "{} - #{}. {}".format(
            self.group.name,
            self.order,
            self.title
        )
