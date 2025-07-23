from django.contrib import admin
from ..models import UserSkill

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ("user", "skill")
    list_filter = ("skill",)
