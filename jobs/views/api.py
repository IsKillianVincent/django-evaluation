import csv
from django.http import HttpResponse
from django.utils.timezone import now
from django.contrib.admin.views.decorators import staff_member_required
from jobs.models import Application

@staff_member_required
def applications_today_csv(request):
    today = now().date()
    applications = Application.objects.filter(created_at__date=today)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=candidatures_du_jour.csv"

    writer = csv.writer(response)
    writer.writerow(["User", "Job", "Date", "Validated"])

    for app in applications:
        writer.writerow([app.user.username, app.job.title, app.created_at.strftime("%Y-%m-%d %H:%M"), app.is_validated])

    return response
