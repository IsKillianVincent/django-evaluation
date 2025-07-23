from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ..models import User, UserSkill, UserLanguage, UserExperience

class UserSkillInline(admin.TabularInline):
    model = UserSkill
    extra = 0

class UserLanguageInline(admin.TabularInline):
    model = UserLanguage
    extra = 0

class UserExperienceInline(admin.StackedInline):
    model = UserExperience
    extra = 0

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "get_full_name", "is_employer", "is_superuser", "is_active")
    list_filter = ("is_employer", "is_superuser", "is_active", "location")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (_("Personal Info"), {
            "fields": ("username", "email", "first_name", "last_name", "photo", "phone", "location", "birth_date", "bio")
        }),
        (_("Professional Info"), {
            "fields": ("linkedin", "website")
        }),
        (_("Permissions"), {
            "fields": ("is_active", "is_staff", "is_superuser", "is_employer", "is_driven", "groups", "user_permissions")
        }),
        (_("Important Dates"), {
            "fields": ("last_login", "date_joined")
        }),
    )

    inlines = [UserSkillInline, UserLanguageInline, UserExperienceInline]

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = _("Full Name")
