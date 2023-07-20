from django.contrib import admin
from .models import *
# Register your models here.
from django.utils.html import format_html
# admin.site.register(Teachers)
from .views import verify_teacher,reject_teacher
from django.contrib.auth.models import Group

class TeacherUserFilter(admin.SimpleListFilter):
    title = 'User'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        return (
            ('teacher', 'Teachers'),
            ('non_teacher', 'Requested Teachers'),
        )

    def queryset(self, request, queryset):
        print(queryset)
        if self.value() == 'teacher':
            return queryset.filter(user__is_student=False, user__is_submit=True,user__is_pending=False)
        if self.value() == 'non_teacher':
            return queryset.filter(user__is_student=False, user__is_submit=True,user__is_pending=True)


class TeacherAdmin(admin.ModelAdmin):
    model = Teachers
    list_display = ['get_user_id','get_user_image', 'get_user_name','get_user_is_teacher', 'get_user_created_at']
    list_display_links = ('get_user_id','get_user_name')

    search_fields = ['user__name']
    list_filter = (TeacherUserFilter,)
    actions = [verify_teacher,reject_teacher]

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.short_description = 'User ID'
    def get_user_is_teacher(self, obj):
        return obj.user.is_teacher
    get_user_id.short_description = 'is_teacher'
    def get_user_image(self,obj):
        image_url = obj.user.image.url if obj.user.image else None
        return format_html('<img src="{}" style="width: 10rem; height: 6rem;" />',image_url) 
    
    get_user_image.short_description = 'User ID'
    get_user_image.allow_tags = True
    def get_user_name(self, obj):
        return obj.user.name

    get_user_name.short_description = 'User Name'

    def get_user_created_at(self, obj):
        return obj.user.date_joined

    get_user_created_at.short_description = 'User Created'
class UserAdmin(admin.ModelAdmin):
    model = UserAccount
    list_display=('id','name','email')
    search_fields=['name','email']
admin.site.register(Teachers, TeacherAdmin)
admin.site.register(UserAccount,UserAdmin)
admin.site.unregister(Group)