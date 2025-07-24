from django.db import models
from django.utils.translation import gettext_lazy as _
from .company import Company

class JobQuerySet(models.QuerySet):
    def open(self):
        return self.filter(is_filled=False)

class JobManager(models.Manager):
    def get_queryset(self):
        return JobQuerySet(self.model, using=self._db)

    def open(self):
        return self.get_queryset().open()

class Job(models.Model):
    ...
    objects = JobManager()


class Job(models.Model):
    title = models.CharField(_("Job Title"), max_length=255)
    description = models.TextField(_("Job Description"))
    location = models.CharField(_("Location"), max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    created_at = models.DateTimeField(auto_now_add=True)
    is_filled = models.BooleanField(default=False)

    objects = JobManager()

    def __str__(self):
        return f"{self.title} @ {self.company.name}"
