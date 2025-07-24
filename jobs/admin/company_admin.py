from django.contrib import admin
from jobs.models import Company, CompanyImage

class CompanyImageInline(admin.TabularInline):
    model = CompanyImage
    extra = 1

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name", "owner__username")
    inlines = [CompanyImageInline]
