from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from .job import Job

class ApplicationQuerySet(models.QuerySet):
    def validated(self):
        return self.filter(is_validated=True)

    def today(self):
        from django.utils.timezone import now
        today = now().date()
        return self.filter(created_at__date=today)

class ApplicationManager(models.Manager):
    def get_queryset(self):
        return ApplicationQuerySet(self.model, using=self._db)

    def validated(self):
        return self.get_queryset().validated()

    def today(self):
        return self.get_queryset().today()

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(_("Cover Letter"), blank=True)
    resume = models.FileField(_("Resume"), upload_to="cvs/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

    objects = ApplicationManager()

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} → {self.job.title}"
