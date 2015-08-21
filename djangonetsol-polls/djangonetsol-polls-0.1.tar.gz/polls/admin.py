from django.contrib import admin

# Register your models here.
from .models import Question, Choice
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    #fields = ['pub_date', 'question_text'] # Set the sequence and display of the fields in form.   
    fieldsets = [
        ('question',               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ] #Add the class collapse to  fields.
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['question_text']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)  #To customize the question form default for admin panel
#admin.site.register(Choice) #for single field means one to one relation ship

