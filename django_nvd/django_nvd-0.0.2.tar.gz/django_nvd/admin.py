from django.contrib import admin
from django_nvd.models import *

admin.site.register(Vulnerability)
admin.site.register(Product)
admin.site.register(ProductVersion)
admin.site.register(VulnerabilitySource)