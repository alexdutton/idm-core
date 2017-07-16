from django.contrib import admin

from . import models

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'label')


admin.site.register(models.Course, CourseAdmin)