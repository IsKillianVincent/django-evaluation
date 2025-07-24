from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib import messages
from jobs.models import Job, Company
from jobs.forms.job_form import JobForm

def job_list(request):
    jobs = Job.objects.filter(is_filled=False).order_by("-created_at")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})

@login_required
@user_passes_test(lambda u: u.is_employer)
def create_job_view(request):
    companies = Company.objects.owned_by(request.user)
    if not companies.exists():
        messages.warning(request, "Vous devez d'abord créer une entreprise avant de pouvoir publier une offre.")
        return redirect("create_company")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            if job.company.owner != request.user:
                messages.error(request, "Vous ne pouvez publier une offre que pour vos propres entreprises.")
                return redirect("dashboard")
            job.save()
            messages.success(request, "Offre publiée avec succès.")
            return redirect("job_list")
    else:
        form = JobForm()

    form.fields["company"].queryset = companies
    return render(request, "jobs/create_job.html", {"form": form})
