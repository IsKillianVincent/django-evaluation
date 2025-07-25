from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from jobs.forms.company_form import CompanyForm, CompanyImagesUploadForm
from jobs.models import Company, CompanyImage
from django.shortcuts import get_object_or_404

@login_required
def create_company_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Seuls les super utilisateurs peuvent créer une entreprise.")
        return redirect("dashboard")

    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        image_form = CompanyImagesUploadForm(request.POST, request.FILES)

        if company_form.is_valid() and image_form.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company.save()

            # Traitement des images (max 5)
            images = request.FILES.getlist('images')
            for img in images[:5]:
                CompanyImage.objects.create(company=company, image=img)

            messages.success(request, "Entreprise créée avec succès.")
            return redirect("company_list")
    else:
        company_form = CompanyForm()
        image_form = CompanyImagesUploadForm()

    return render(request, "jobs/create_company.html", {
        "company_form": company_form,
        "image_form": image_form,
    })

def company_list_view(request):
    companies = Company.objects.prefetch_related("images").all()
    return render(request, "jobs/company_list.html", {"companies": companies})

@login_required
def update_company_view(request, pk):
    company = get_object_or_404(Company, pk=pk, owner=request.user)

    if request.method == "POST":
        company_form = CompanyForm(request.POST, instance=company)
        image_form = CompanyImagesUploadForm(request.POST, request.FILES)

        if company_form.is_valid() and image_form.is_valid():
            company_form.save()

            new_images = request.FILES.getlist('images')
            for img in new_images[:5]:
                CompanyImage.objects.create(company=company, image=img)

            messages.success(request, "Entreprise mise à jour avec succès.")
            return redirect("company_list")
    else:
        company_form = CompanyForm(instance=company)
        image_form = CompanyImagesUploadForm()

    return render(request, "jobs/update_company.html", {
        "company_form": company_form,
        "image_form": image_form,
        "company": company,
    })