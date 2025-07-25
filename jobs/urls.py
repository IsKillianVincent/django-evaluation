from django.urls import path
from jobs.views.job_views import JobListView, JobDetailView, CreateJobView
from jobs.views.application_views import SubmitApplicationView, UserApplicationsView
from jobs.views.employer_views import EmployerDashboardView, ValidateApplicationView, InvalidateApplicationView
from jobs.views.company_views import company_list_view, create_company_view, update_company_view
from jobs.views.api import applications_today_csv
from jobs.views.notification_views import notification_list_view, mark_notification_as_read_view, unread_notification_count

urlpatterns = [
    path("", JobListView.as_view(), name="job_list"),
    path("job/<int:pk>/", JobDetailView.as_view(), name="job_detail"),
    path("job/create/", CreateJobView.as_view(), name="create_job"),

    path("apply/<int:job_id>/", SubmitApplicationView.as_view(), name="submit_application"),
    path("my-applications/", UserApplicationsView.as_view(), name="user_applications"),
    path("employer/dashboard/", EmployerDashboardView.as_view(), name="employer_dashboard"),
    path("application/<int:app_id>/validate/", ValidateApplicationView.as_view(), name="validate_application"),
    path("application/<int:app_id>/invalidate/", InvalidateApplicationView.as_view(), name="invalidate_application"),

    path("companies/", company_list_view, name="company_list"),
    path("companies/create/", create_company_view, name="create_company"),
    path("company/<int:pk>/edit/", update_company_view, name="update_company"),

    path("export/applications-today/", applications_today_csv, name="applications_today_csv"),

    path("notifications/", notification_list_view, name="notification_list"),
    path("notifications/<int:pk>/read/", mark_notification_as_read_view, name="mark_notification_read"),
    path("api/notifications/unread_count/", unread_notification_count, name="unread_notifications"),

]
