
from ..cat263 import Cat263, MDRd, NkRd
from ...results import Results


class Amazius(Results):
	code = 'SIA 263:13'
	selection = ['nrd', 'vrd', 'mrdy', 'mrdz', 'mdrd', 'nkrd_y', 'nkrd_z']

	def __init__(self, entries):

		self.cat = Cat263(entries)
		self.cross_section_class = entries['cross_section_class']
		self.ned = entries['ned']*1e3
		self.ved = entries['ved']*1e3
		self.medy = entries['medy']*1e6
		self.medz = entries['medz']*1e6
		self.entries = entries
		
	def add_sel(self, sel):
		if sel not in self.selection:
			self.selection.append(sel)
		

	def compute(self):
		mdrd = MDRd(self.entries)
		mdrd.mdrd()
		nkrd = NkRd(self.entries)
		nkrd.nkrd_y()
		nkrd.nkrd_z()
		
		if self.cross_section_class == '1 + 2':
			self.class_1()

		return  self.get_results()

	def class_1(self):
		self.cat.nrd()
		self.cat.mrdy()
		self.cat.mrdz()
		self.cat.vrd()

		if self.ved > 0:
			self.cat.mvrd(self.ved)
			self.add_sel('mvrd')
			
		if self.ned > 0 and self.medy > 0 and self.medz > 0:
			self.cat.f44(self.ned, self.medy, self.medz)
			self.add_sel('f44')
			
		if self.ned > 0 and self.medy > 0:
			self.cat.mynrd(self.ned)
			self.add_sel('mynrd')
		
		
		



	def vrd(self):
		pass



 
