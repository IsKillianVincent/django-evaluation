from django.db import models
from accounts.models.user import User

class CompanyQuerySet(models.QuerySet):
    def owned_by(self, user):
        return self.filter(owner=user)

class CompanyManager(models.Manager):
    def get_queryset(self):
        return CompanyQuerySet(self.model, using=self._db)

    def owned_by(self, user):
        return self.get_queryset().owned_by(user)

class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CompanyManager()

    def __str__(self):
        return self.name
