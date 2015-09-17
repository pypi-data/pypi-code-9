from django.contrib import admin

from mezzanine.pages.admin import PageAdmin
from .models import HomePage, Slide, Portfolio, PortfolioItem, PortfolioItemImage, PortfolioItemCategory, Porter, TempPortfolio, ItemPorter, Portfolios, DocumentListItem, DocumentList, DocumentListItemCategory
from mezzanine.core.admin import TabularDynamicInlineAdmin

class SlideInline(TabularDynamicInlineAdmin):
    model = Slide

class PorterInline(TabularDynamicInlineAdmin):
    model = Porter

class ItemPorterInline(TabularDynamicInlineAdmin):
    model = ItemPorter

class HomePageAdmin(PageAdmin):
	inlines = (SlideInline, PorterInline,)

class TempPortfolioAdmin(PageAdmin):
	inlines = (ItemPorterInline,)

class PortfolioItemImageInline(TabularDynamicInlineAdmin):
    model = PortfolioItemImage

class PortfolioItemAdmin(PageAdmin):
    inlines = (PortfolioItemImageInline,)
    
class DocumentListItemInline(TabularDynamicInlineAdmin):
	model = DocumentListItem
	
class DocumentListAdmin(PageAdmin):
	inlines = (DocumentListItemInline,)
	
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(TempPortfolio, TempPortfolioAdmin)
admin.site.register(Portfolio, PageAdmin)
admin.site.register(Portfolios, PageAdmin)
admin.site.register(PortfolioItemCategory)
admin.site.register(PortfolioItem, PortfolioItemAdmin)
admin.site.register(DocumentList, DocumentListAdmin)
admin.site.register(DocumentListItemCategory)
