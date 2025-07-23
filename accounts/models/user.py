from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date

def user_directory_path(instance, filename):
    return f'users/{instance.id}/{filename}'

class User(AbstractUser):
    first_name = models.CharField(_("First Name"), max_length=150)
    last_name = models.CharField(_("Last Name"), max_length=150)
    email = models.EmailField(_("Email Address"), unique=True)
    
    photo = models.ImageField(_("Profile Photo"), upload_to=user_directory_path, blank=True, null=True)
    location = models.CharField(_("Place of Residence"), max_length=255, blank=True)
    phone = models.CharField(_("Mobile"), max_length=20, blank=True)
    birth_date = models.DateField(_("Birth Date"), blank=True, null=True)
    bio = models.TextField(_("About Me"), blank=True)

    linkedin = models.URLField(_("LinkedIn URL"), blank=True)
    website = models.URLField(_("Personal Website"), blank=True)

    is_employer = models.BooleanField(_("Is Employer?"), default=False)
    is_driven = models.BooleanField(_("Is Driven?"), default=False)

    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} ({self.get_full_name()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
