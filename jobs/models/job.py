from django.db import models
from django.utils.translation import gettext_lazy as _
from .company import Company

class Job(models.Model):
    title = models.CharField(_("Job Title"), max_length=255)
    description = models.TextField(_("Job Description"))
    location = models.CharField(_("Location"), max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"
