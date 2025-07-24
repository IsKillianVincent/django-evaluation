from django.contrib import admin
from jobs.models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "location", "is_filled", "created_at")
    list_filter = ("is_filled", "company")
    search_fields = ("title", "company__name", "location")
    ordering = ("-created_at",)
