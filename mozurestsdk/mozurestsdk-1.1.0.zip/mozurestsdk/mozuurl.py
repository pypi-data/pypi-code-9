from mozurestsdk.urllocation import UrlLocation;

class MozuUrl(object):
	def __init__(self, uri, verb, location: UrlLocation, useSSL ):
		self.uri = uri.lower();
		self.location = location;
		self.useSSL = useSSL;
		self.verb = verb;

	def formatUrl(self, paramName, value):
		paramName = paramName.lower();

		self.uri = self.uri.replace("{"+paramName+"}", "" if (value is None) else str(value));
		self.uri = self.uri.replace("{*"+paramName+"}", "" if (value is None) else str(value));
		removeStr = "&"+paramName+"=";
		if (value is None and self.uri.find(removeStr)):
			self.uri = self.uri.replace(removeStr, "");

		removeStr = paramName+"=";
		if (value is None and self.uri.find(removeStr)):
			self.uri = self.uri.replace(removeStr, "");

		removeStr = "/?";
		if (self.uri.endswith(removeStr)):
			self.uri = self.uri.replace(removeStr, "");

		if (self.uri.endswith(removeStr+"&")):
			self.uri = self.uri.replace(removeStr, "");
		
		if (self.uri.endswith("&")):
			self.uri = self.uri.replace("&", "");

		if (self.uri.find("/?&")):
			self.uri = self.uri.replace("/?&", "/?");

		if (self.uri.endswith("?")):
			self.uri = self.uri.replace("?", "");