from django.db import models
from .company import Company

def company_image_upload_path(instance, filename):
    return f"companies/{instance.company.id}/{filename}"

class CompanyImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=company_image_upload_path)
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.company.name}"
