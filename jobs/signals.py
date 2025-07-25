from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import Application
from .models.notification import Notification

@receiver(post_save, sender=Application)
def notify_recruiter_on_application(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        recruiter = job.company.owner

        Notification.objects.create(
            user=recruiter,
            message=f"{instance.user.get_full_name()} a postulé à votre offre « {job.title} »."
        )