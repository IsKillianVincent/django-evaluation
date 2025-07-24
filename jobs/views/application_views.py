from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from jobs.models import Job, Application
from jobs.forms.application_form import ApplicationForm

def is_employer(user):
    return user.is_authenticated and user.is_employer

@login_required
def submit_application(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(user=request.user, job=job).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect("job_detail", pk=job.id)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.job = job
            app.save()
            messages.success(request, "Votre candidature a été envoyée.")
            return redirect("user_applications")
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply.html", {"form": form, "job": job})


@login_required
def user_applications(request):
    applications = request.user.applications.select_related("job", "job__company").order_by("-created_at")
    return render(request, "jobs/user_applications.html", {"applications": applications})


@user_passes_test(lambda u: u.is_superuser)
def employer_dashboard(request):
    applications = Application.objects.filter(job__company__owner=request.user).select_related("job", "user")
    return render(request, "jobs/employer_dashboard.html", {"applications": applications})

@login_required
@user_passes_test(is_employer)
def validate_application(request, app_id):
    app = Application.objects.select_related("job__company").filter(id=app_id).first()
    if app and app.job.company.owner == request.user:
        app.is_validated = True
        app.save()
        messages.success(request, "Candidature validée.")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect("employer_dashboard")


@login_required
@user_passes_test(is_employer)
def invalidate_application(request, app_id):
    app = Application.objects.select_related("job__company").filter(id=app_id).first()
    if app and app.job.company.owner == request.user:
        app.is_validated = False
        app.save()
        messages.success(request, "Candidature invalidée.")
    else:
        messages.error(request, "Action non autorisée.")
    return redirect("employer_dashboard")