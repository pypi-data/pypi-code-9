from django.contrib import admin
from models.facebook import Facebook
from models.twitter import Twitter
from models.linkedin import Linkedin

@admin.register(Facebook)
class FacebookAdmin(admin.ModelAdmin):
    pass

@admin.register(Twitter)
class TwitterAdmin(admin.ModelAdmin):
    pass

@admin.register(Linkedin)
class LinkedinAdmin(admin.ModelAdmin):
    pass

# admin.site.register(Facebook)
# admin.site.register(Twitter)
# admin.site.register(Linkedin)