from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.pages.models import Page
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.utils.models import upload_to

class HomePage(Page, RichText):
	
    logo = FileField(verbose_name=_("Logo"),
        upload_to=upload_to("theme.HomePage.image", "logo"),
        format="Image", max_length=255, null=True, blank=True)
    quote = models.CharField(max_length=2000, blank=True, null=True,
	    help_text="Quote text (optional)")
    quote_author = models.CharField(max_length=2000, blank=True, null=True,
	    help_text="Quote authors name")
    quote_link = models.CharField(max_length=2000, blank=True, null=True,
	    help_text="link to the author of the quote's site (optional)")
	    
    class Meta:
		verbose_name = _("Home page")
		verbose_name_plural = _("Home pages")
		
class Porter(Orderable):
    '''
    more portfolio's to the home page
    '''
    
    homepage = models.ForeignKey(HomePage, blank=True, null=True, related_name="porter")
    multiport = models.ForeignKey("Portfolio", blank=True, null=True,
        help_text="If selected items from this portfolio will be featured "
                  "on the home page.")

class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.Slide.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)
    featured_image = models.NullBooleanField(blank=True, help_text="The active 1st image to appear")
    main_label = models.CharField(max_length=2000, blank=True, null=True)
    sub_label = models.CharField(max_length=2000, blank=True, null=True)
    
class Portfolios(Page, RichText):
	'''
	A collection of portfolio items
	'''
	
	class Meta:
		verbose_name = _("Portfolios")
		verbose_name_plural = _("Portfolios'")

class Portfolio(Page):
    '''
    A collection of individual portfolio items
    '''
    portfolio_item = models.ForeignKey("PortfolioItem", blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")

class TempPortfolio(Page):
	'''
	A temp. portfolio, with a collection of selected portfolio items
	'''
	content = RichTextField(blank=True, null=True)
	
	class Meta:
		verbose_name = _("TempPortfolio")
		verbose_name_plural = _("TempPortfolios")

class ItemPorter(Orderable):
	'''
	Portfolio items for TempPortfolio
	'''
	temp_portfolio = models.ForeignKey(TempPortfolio, related_name="item_porter", blank=True, null=True)
	portfolio_item = models.ForeignKey("PortfolioItem", blank=True, null=True,
	    help_text="If selected portfolio items will be featured on this porfolio")

class PortfolioItem(Page, RichText):
    '''
    An individual portfolio item, should be nested under a Portfolio
    '''
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("theme.PortfolioItem.featured_image", "portfolio"),
        format="Image", max_length=255, null=True, blank=True)
    short_description = RichTextField(blank=True)
    categories = models.ManyToManyField("PortfolioItemCategory",
                                        verbose_name=_("Categories"),
                                        blank=True,
                                        related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,
        help_text="A link to the finished project (optional)")

    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")

class PortfolioItemImage(Orderable):
    '''
    An image for a PortfolioItem
    '''
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("theme.PortfolioItemImage.file", "portfolio items"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """

    class Meta:
        verbose_name = _("Portfolio Item Category")
        verbose_name_plural = _("Portfolio Item Categories")
        ordering = ("title",)

class DocumentList(Page, RichText):
	'''
	A collection of Document list items
	'''
	heading = models.CharField(max_length=250,
	    help_text="The heading for the Document list")
	    
class DocumentListItemCategory(Slugged):
	'''
	A category for grouping document items into categories
	'''
	
	class Meta:
		verbose_name = _("Document List Item Category")
		verbose_name_plural = _("Document List Item Categories")
		ordering = ("title",)
		
class DocumentListItem(Orderable):
	'''
	Individual documents for document list
	'''
	
	documentlist = models.ForeignKey(DocumentList, related_name="documents", blank=True, null=True)
	files = FileField(verbose_name=_("File"), null=True, blank=True,
	    upload_to=upload_to("theme.DocumentListItem.file", "documents"))
	title = models.CharField(max_length=200)
	category = models.ForeignKey(DocumentListItemCategory, related_name="category", blank=True, null=True)
	    
