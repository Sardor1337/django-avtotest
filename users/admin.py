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

    def get_queryset(self, request):
        """ Superadmin bo‘lmaganlar superuserlarni ko‘rmasligi uchun querysetni filter qilamiz """
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(is_superuser=False)  # Superadmin bo‘lmaganlarga faqat oddiy userlarni ko‘rsatamiz
        return qs

    def get_fieldsets(self, request, obj=None):
        """ Agar obj mavjud bo‘lmasa (yangi user qo‘shilayotgan bo‘lsa), add_fieldsetsni ishlatamiz """
        if not obj:
            return self.add_fieldsets  # Yangi foydalanuvchi qo‘shilayotganda `add_fieldsets` ishlaydi

        # Superadmin bo'lmasa, `first_name` va `last_name` yashiriladi
        if request.user.is_superuser:
            return (
                (None, {'fields': ('password',)}),
                ('Personal info', {'fields': ('phone_number', 'user_role')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
                ('Misc', {'fields': ('end_time',)}),
            )
        else:
            return (
                (None, {'fields': ('password',)}),
                ('Personal info', {'fields': ('phone_number', 'user_role')}),
                # first_name va last_name olib tashlandi
                ('Permissions', {'fields': ('is_active',)}),
                ('Misc', {'fields': ('end_time',)}),
            )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'password1', 'password2', 'end_time', 'is_active', 'user_role')}),
    )



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserRole)
admin.site.register(Table)
admin.site.register(Correct)
admin.site.register(Answers)
admin.site.register(Checkbox)
admin.site.register(Questions)
admin.site.register(Category)
