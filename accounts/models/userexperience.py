from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

class UserExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(_("Job Title"), max_length=255)
    company = models.CharField(_("Company"), max_length=255)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    is_current = models.BooleanField(_("Currently Working"), default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"
