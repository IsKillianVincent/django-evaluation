from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from jobs.models import Job, Application
from jobs.forms import ApplicationForm

class SubmitApplicationView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "jobs/apply.html"

    def dispatch(self, request, *args, **kwargs):
        self.job = get_object_or_404(Job, pk=self.kwargs["job_id"])
        if Application.objects.filter(user=request.user, job=self.job).exists():
            messages.warning(request, "Vous avez déjà postulé à cette offre.")
            return redirect("job_detail", pk=self.job.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.job = self.job
        messages.success(self.request, "Candidature envoyée.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = self.job
        return context

    def get_success_url(self):
        return "/jobs/my-applications/"

class UserApplicationsView(LoginRequiredMixin, ListView):
    model = Application
    template_name = "jobs/user_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        return self.request.user.applications.select_related("job", "job__company").order_by("-created_at")
