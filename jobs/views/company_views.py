from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from jobs.forms.company_form import CompanyForm, CompanyImageForm
from jobs.models import Company, CompanyImage

@login_required
def create_company_view(request):
    if not request.user.is_superuser:
        messages.error(request, "Seuls les super utilisateurs peuvent créer une entreprise.")
        return redirect("dashboard")

    ImageFormSet = modelformset_factory(CompanyImage, form=CompanyImageForm, extra=3, max_num=5, can_delete=False)

    if request.method == "POST":
        company_form = CompanyForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=CompanyImage.objects.none())

        if company_form.is_valid() and formset.is_valid():
            company = company_form.save(commit=False)
            company.owner = request.user
            company.save()

            for form in formset.cleaned_data:
                if form and form.get("image"):
                    CompanyImage.objects.create(
                        company=company,
                        image=form["image"],
                        caption=form.get("caption", "")
                    )

            messages.success(request, "Entreprise créée avec succès.")
            return redirect("company_list")
    else:
        company_form = CompanyForm()
        formset = ImageFormSet(queryset=CompanyImage.objects.none())

    return render(request, "jobs/create_company.html", {
        "company_form": company_form,
        "formset": formset,
    })


def company_list_view(request):
    companies = Company.objects.prefetch_related("images").all()
    return render(request, "jobs/company_list.html", {"companies": companies})
