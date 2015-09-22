from django.contrib import admin
from .models import SwiftFile, SwiftContainer
from .forms import SwiftFileForm

# Register your models here.
class SwiftContainerAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		SwiftContainer.create_container(title=obj.title)

class SwiftFileAdmin(admin.ModelAdmin):
	exclude=['date_created', 'filename', 'author', 'filesize', 'content_type', 'container', 'date_modified', 'temp_url', 'key']
	form = SwiftFileForm
	actions = ['delete_selected']

	def save_model(self, request, obj, form, change):
		data = form.cleaned_data['filefield']
		filename=data.name
		content_type = data.content_type
		obj = SwiftFile.upload_file(file_contents=data.read(), filename=filename, content_type=content_type)
		return obj

	def delete_selected(modeladmin, request, queryset):
	    for obj in queryset.all():
	        obj.delete()
		
admin.site.register(SwiftContainer, SwiftContainerAdmin)
admin.site.register(SwiftFile, SwiftFileAdmin)
