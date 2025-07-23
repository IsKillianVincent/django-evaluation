from django.db import models
from .user import User
from .language import Language
from django.utils.translation import gettext_lazy as _

class UserLanguage(models.Model):
    LEVEL_CHOICES = [
        ('A1', _('Beginner (A1)')),
        ('A2', _('Elementary (A2)')),
        ('B1', _('Intermediate (B1)')),
        ('B2', _('Upper Intermediate (B2)')),
        ('C1', _('Advanced (C1)')),
        ('C2', _('Proficient (C2)')),
        ('FLUENT', _('Fluent')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    level = models.CharField(_("Proficiency Level"), max_length=10, choices=LEVEL_CHOICES)

    class Meta:
        unique_together = ('user', 'language')
        verbose_name = _("User Language")
        verbose_name_plural = _("User Languages")

    def __str__(self):
        return f"{self.user.username} - {self.language.name} ({self.level})"
