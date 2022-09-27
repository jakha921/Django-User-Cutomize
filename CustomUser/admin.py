from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    readonly_fields = ('date_joined', 'last_login')

    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'groups', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (None, {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        (None, {
            'fields': ('groups', 'user_permissions',)
        }),
        ("Dates", {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
