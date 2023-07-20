from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id','name','is_publish']
    list_display_links = ['id','name']
    search_fields = ['name']
class CourseAdmin(admin.ModelAdmin):
    model = Course
    list_display = ['id', 'title', 'display_categories', 'is_publish']
    list_display_links = ['id', 'title']
    search_fields = ['title']
    # list_editable = ['is_publish']
    def display_categories(self, obj):
        return ", ".join([str(category) for category in obj.cat.all()])
    display_categories.short_description = 'Categories'

admin.site.register(Category,CategoryAdmin)
admin.site.register(Course,CourseAdmin)