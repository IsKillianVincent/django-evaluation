from django.contrib import admin
from accounts.models import UserExperience

@admin.register(UserExperience)
class UserExperienceAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "company", "start_date", "end_date")
    search_fields = ("title", "company", "user__username")
    list_filter = ("start_date", "end_date")
