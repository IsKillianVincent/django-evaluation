from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from jobs.models import Application

class EmployerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_employer

class EmployerDashboardView(EmployerRequiredMixin, View):
    def get(self, request):
        apps = Application.objects.filter(
    job__company__owner=request.user
).select_related("job", "job__company", "user").prefetch_related(
    "user__skills", "user__languages"
)
        return render(request, "jobs/employer_dashboard.html", {"applications": apps})

class ValidateApplicationView(EmployerRequiredMixin, View):
    def post(self, request, app_id):
        app = get_object_or_404(Application, pk=app_id, job__company__owner=request.user)
        app.is_validated = True
        app.save()
        messages.success(request, "Candidature validée.")
        return redirect("employer_dashboard")

class InvalidateApplicationView(EmployerRequiredMixin, View):
    def post(self, request, app_id):
        app = get_object_or_404(Application, pk=app_id, job__company__owner=request.user)
        app.is_validated = False
        app.save()
        messages.success(request, "Candidature invalidée.")
        return redirect("employer_dashboard")
