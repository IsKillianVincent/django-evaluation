from django.contrib import admin
from django.http import HttpResponse
import csv
from jobs.models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at", "is_validated")
    list_filter = ("is_validated", "created_at", "job")
    search_fields = ("user__username", "job__title")
    actions = ["export_as_csv", "mark_as_validated"]

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=candidatures.csv"
        writer = csv.writer(response)
        writer.writerow(["User", "Job", "Date", "Validated"])

        for app in queryset:
            writer.writerow([app.user.username, app.job.title, app.created_at, app.is_validated])

        return response

    export_as_csv.short_description = "Exporter en CSV"

    def mark_as_validated(self, request, queryset):
        updated = queryset.update(is_validated=True)
        self.message_user(request, f"{updated} candidature(s) validée(s).")

    mark_as_validated.short_description = "Valider les candidatures"
