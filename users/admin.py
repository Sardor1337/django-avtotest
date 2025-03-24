from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.exceptions import ValidationError

from .models import CustomUser, UserRole, Table, Correct, Answers, Checkbox, Questions, Category


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'phone_number', 'is_active', 'create_time', 'end_time']
    list_filter = ['is_active', 'user_role']
    search_fields = ['phone_number']
    ordering = ['id']

    # `fieldsets` ni yangilash, takrorlanmasligini ta'minlash
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'user_role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Misc', {'fields': ('end_time',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2', 'end_time' , 'is_active', 'is_staff', 'user_role')}),
    )



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserRole)
admin.site.register(Table)
admin.site.register(Correct)
admin.site.register(Answers)
admin.site.register(Checkbox)
admin.site.register(Questions)
admin.site.register(Category)
