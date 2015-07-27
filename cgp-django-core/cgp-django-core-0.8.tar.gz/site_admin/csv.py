from django.utils import timezone
from django.contrib import messages

from .utils.csv_output import ModelToCSV

def output_csv(modeladmin, request, queryset):
	

	try:

		verbose_name = modeladmin.model._meta.verbose_name_plural.title()
		now = timezone.now()
		now_string ="%s-%s-%s" % (now.year, str(now.month).zfill(2), str(now.day).zfill(2))
		filename = "%s_%s.csv" % (verbose_name, now_string)

		return ModelToCSV(request, queryset, modeladmin.csv_fields, filename=filename)

	except:
		messages.warning(request, 'There are no CSV fields specified for this model')
	    

output_csv.short_description = "Output to CSV"


