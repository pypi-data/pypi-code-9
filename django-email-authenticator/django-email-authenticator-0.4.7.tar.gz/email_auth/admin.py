from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

class EmailUserAdmin(admin.ModelAdmin):
    class Meta:
        model = get_user_model()

admin.site.register(get_user_model(), EmailUserAdmin)