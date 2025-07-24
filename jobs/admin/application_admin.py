from django.contrib import admin
from django.utils import timezone
from django.http import HttpResponse
from import_export.admin import ImportExportMixin
import csv
from accounts.models import User
from jobs.models import Job

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from jobs.models import Application, Job

class ApplicationResource(resources.ModelResource):
    user__username = fields.Field(
        column_name="user__username",
        attribute="user",
        widget=ForeignKeyWidget(User, "username")
    )
    job__title = fields.Field(
        column_name="job__title",
        attribute="job",
        widget=ForeignKeyWidget(Job, "title")
    )

    class Meta:
        model = Application
        fields = ("user__username", "job__title", "cover_letter", "is_validated")
        import_id_fields = ("user__username", "job__title")

    def before_import_row(self, row, **kwargs):
        username = row.get("user__username")
        job_title = row.get("job__title")

        if not User.objects.filter(username=username).exists():
            raise ValueError(f"Utilisateur '{username}' introuvable")

        if not Job.objects.filter(title=job_title).exists():
            raise ValueError(f"Offre '{job_title}' introuvable")

    def get_instance(self, instance_loader, row):
        """
        Empêche la création d'un doublon user+job si déjà existant.
        """
        username = row.get("user__username")
        job_title = row.get("job__title")

        try:
            user = User.objects.get(username=username)
            job = Job.objects.get(title=job_title)
            return Application.objects.filter(user=user, job=job).first()
        except (User.DoesNotExist, Job.DoesNotExist):
            return None


@admin.register(Application)
class ApplicationAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ApplicationResource

    list_display = ("user", "job", "created_at", "is_validated")
    list_filter = ("is_validated", "created_at", "job")
    search_fields = ("user__username", "job__title")
    actions = ["export_today_csv", "mark_as_validated"]

    def export_today_csv(self, request, queryset):
        today = timezone.now().date()
        apps_today = Application.objects.filter(created_at__date=today)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=candidatures_du_jour.csv"
        writer = csv.writer(response)
        writer.writerow(["Username", "Job", "Cover Letter", "Date", "Validated"])

        for app in apps_today:
            writer.writerow([
                app.user.username,
                app.job.title,
                app.cover_letter,
                app.created_at.strftime("%Y-%m-%d %H:%M"),
                "Oui" if app.is_validated else "Non"
            ])
        return response

    export_today_csv.short_description = "Exporter les candidatures du jour (CSV)"

    def mark_as_validated(self, request, queryset):
        updated = queryset.update(is_validated=True)
        self.message_user(request, f"{updated} candidature(s) validée(s).")

    mark_as_validated.short_description = "Valider les candidatures"
