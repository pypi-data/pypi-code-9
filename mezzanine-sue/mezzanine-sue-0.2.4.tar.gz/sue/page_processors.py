from mezzanine.pages.page_processors import processor_for
from .models import Portfolio, PortfolioItem, PortfolioItemCategory, HomePage, TempPortfolio, Portfolios, DocumentList, DocumentListItem, DocumentListItemCategory

@processor_for(Portfolios)
def portfolios_processor(request, page):
	'''
	Adds portfolio context to portfolios page
	'''
	portfolios = Portfolio.objects.published(
	    for_user=request.user).select_related().all()
	portfolios = portfolios.filter(parent=page) ##porfolio pages need to nested under here
	return {'portfolios': portfolios}

@processor_for(Portfolio)
def portfolio_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    # get the Portfolio's items, prefetching categories for performance
    items = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related('categories')
    items = items.filter(parent=page)
    # filter out only cateogries that are user in the Portfolio's items
    categories = PortfolioItemCategory.objects.filter(
        portfolioitems__in=items).distinct()
    return {'items': items, 'categories': categories}
    
@processor_for(PortfolioItem)
def portfolioitem_processor(request, page):
    '''
    Adds a portfolio's portfolio items to the context
    '''
    portfolioitem = PortfolioItem.objects.published(
        for_user=request.user).prefetch_related(
        'categories', 'images').get(id=page.portfolioitem.id)
    return {'portfolioitem': portfolioitem}
    
@processor_for(HomePage)
def home_processor(request, page):
    items = PortfolioItem.objects.published(
        for_user=request.user).select_related().all()
    # manually select portfolio pages
    portfolio = Portfolio.objects.published(
        for_user=request.user).select_related().all()
    temp_portfolio = TempPortfolio.objects.published(
        for_user=request.user).select_related().all()
    temp_portfolio = temp_portfolio.filter(parent=page) ##TempPorfolio should be nested under the HomePage
    return {'items': items, 'portfolio': portfolio,
            'temp_portfolio': temp_portfolio}

@processor_for(DocumentList)
def documentlist_processor(request, page):

    category = DocumentListItemCategory.objects.all()
    items = DocumentListItem.objects.filter(documentlist_id=page.documentlist.id)

    return {'category': category, 'items': items}
