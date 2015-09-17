from django.test import TestCase, Client
from theme.models import Page, HomePage, Portfolio, PortfolioItem, Portfolios
# Test user interaction, to the best of our ability
# create tests that can be tested across websites, with altering template design
# Test template context

'''class SimpleTest(TestCase):
    def test_details(self):
        response = self.client.get('/customer/details/')
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get('/customer/index/')
        self.assertEqual(response.status_code, 200)'''
        
# Testing Models and context	
class PageTest(TestCase):
	def setUp(self):
		Page.objects.create(slug="/")
	    
	def test_page_creation(self):
		page = Page.objects.get(slug="/")
		self.assertEqual(page.slug, "/")
		
class HomePageTest(TestCase):
	def setUp(self):
		HomePage.objects.create(title="test")
		
	def test_homepage_creation(self):
		homepage = HomePage.objects.get(title="test")
		self.assertEqual(homepage.title, "test")
		
class PortfolioTest(TestCase):
	def setUp(self):
		Portfolio.objects.create(slug="portfolio")
		
	def test_portfolio_creation(self):
		portfolio = Portfolio.objects.get(slug="portfolio")
		self.assertEqual(portfolio.slug, "portfolio")

class PortfolioItemTest(TestCase):
	def setUp(self):
		PortfolioItem.objects.create(slug="portfolioitem")
		
	def test_portfolioitem_creation(self):
		portfolio_item = PortfolioItem.objects.get(slug="portfolioitem")
		self.assertEqual(portfolio_item.slug, "portfolioitem")

class PortfoliosTest(TestCase):
	def setUp(self):
		Portfolios.objects.create(slug="portfolios")
		
	def test_portfolios_creation(self):
		portfolios = Portfolios.objects.get(slug="portfolios")
		self.assertEqual(portfolios.slug, "portfolios")
