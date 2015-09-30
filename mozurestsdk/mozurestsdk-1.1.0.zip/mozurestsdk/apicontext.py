from mozurestsdk import util;

class ApiContext():
	def __init__(self, options=None,**args):
		args = util.merge_dict(options or {}, args);
		self.tenantId = args.get("tenantId", None);
		self.siteId = args.get("siteId", None);
		self.catalogId = args.get("catalogId", None);
		self.masterCatalogId = args.get("masterCatalogId", None);
		self.tenantUrl = args.get("tenantUrl", None);
		self.locale = args.get("locale", None);
		self.currency = args.get("currency", None);
		self.userClaim = args.get("userClaim", None);
		self.dataViewMode = args.get("dataViewMode",None);
