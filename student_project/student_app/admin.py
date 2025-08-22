from django.contrib import admin
from .models import student_record

# Register your models here.

class recordAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','gender','course')

admin.site.register(student_record,recordAdmin)