from django.db import models
from .user import User
from .skill import Skill
from django.utils.translation import gettext_lazy as _

class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'skill')
        verbose_name = _("User Skill")
        verbose_name_plural = _("User Skills")

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"
