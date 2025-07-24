from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

from jobs.models import Job, Company
from jobs.forms import JobForm

class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"

    def get_queryset(self):
        return Job.objects.filter(is_filled=False).order_by("-created_at")

class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"

class CreateJobView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/create_job.html"

    def test_func(self):
        return self.request.user.is_employer

    def dispatch(self, request, *args, **kwargs):
        companies = Company.objects.owned_by(request.user)
        if not companies.exists():
            messages.warning(request, "Vous devez d’abord créer une entreprise.")
            return redirect("create_company")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["company"].queryset = Company.objects.owned_by(self.request.user)
        return form

    def form_valid(self, form):
        if form.instance.company.owner != self.request.user:
            messages.error(self.request, "Vous ne pouvez publier que pour vos entreprises.")
            return redirect("dashboard")
        messages.success(self.request, "Offre créée avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or "/jobs/"
