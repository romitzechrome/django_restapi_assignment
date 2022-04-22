from django.contrib import admin
from .models import *

admin.site.site_header = 'Online Assigment Submission'


class AssigmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'Name', 'Questions', 'Created_date', 'Deadline', 'course')


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('id', 'ass', 'title', 'answer', 'created_date', 'points', 'comments', 'user')


admin.site.register(Course)
admin.site.register(Assigment, AssigmentAdmin)
admin.site.register(Solution, SolutionAdmin)
