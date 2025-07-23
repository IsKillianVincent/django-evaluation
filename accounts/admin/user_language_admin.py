from django.contrib import admin
from accounts.models import UserLanguage

@admin.register(UserLanguage)
class UserLanguageAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "level")
    list_filter = ("language", "level")