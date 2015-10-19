from django.db import models

class Product(models.Model):
	type = models.CharField(max_length=1)
	vendor = models.CharField(max_length=100)
	name = models.CharField(max_length=100)

	class Meta:
		unique_together = ("vendor","name")

	def __str__(self):
		return "%s %s" % (self.vendor, self.name)

class ProductVersion(models.Model):
	product = models.ForeignKey(Product)
	version = models.CharField(max_length=50, blank=True)

	class Meta:
		unique_together = ("product","version")

	def __str__(self):
		return "%s %s" % (self.product, self.version)

	def get_full_name(self):
		return str(self)

class Vulnerability(models.Model):
	cve = models.CharField(max_length=50, unique=True)
	released_on = models.DateField()
	description = models.TextField()
	cvss = models.CharField(max_length=75, blank=True)
	product_version = models.ManyToManyField(ProductVersion)

	def __str__(self):
		return self.cve

	def references(self):
		aux = []
		for row in VulnerabilitySource.objects.filter(vulnerability=self):
			aux.append(row.url)
		return aux

class VulnerabilitySource(models.Model):
	vulnerability = models.ForeignKey(Vulnerability)
	url = models.URLField(max_length=500)