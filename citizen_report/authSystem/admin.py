from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {"fields": ("email", "username", "department", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "department", "password1", "password2", "is_staff",
                "is_active", "user_permissions"
            )}
         ),
    )
    list_display = ("email", "username", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, CustomUserAdmin)
