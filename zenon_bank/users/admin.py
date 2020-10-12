from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student, Profile


class StudentInline(admin.StackedInline):
    model = Student
    can_delete=True
    verbose_name_plural= "Students"

class UserAdmin(BaseUserAdmin):
    inlines=(StudentInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register([Profile])

