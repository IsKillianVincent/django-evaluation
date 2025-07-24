from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models.user import User
from .job import Job

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    cover_letter = models.TextField(_("Cover Letter"), blank=True)
    resume = models.FileField(_("Resume"), upload_to="cvs/")
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} → {self.job.title}"
