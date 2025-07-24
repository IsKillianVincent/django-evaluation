from django.db.models.signals import post_save
from django.dispatch import receiver
from jobs.models import Application
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Application)
def notify_employer_on_application(sender, instance, created, **kwargs):
    if created:
        job = instance.job
        employer = job.company.owner

        subject = f"Nouvelle candidature pour {job.title}"
        message = (
            f"{instance.user.get_full_name()} a postulé à votre offre \"{job.title}\".\n"
            f"Lettre de motivation :\n{instance.cover_letter}"
        )

        print(f"[SIGNAL] Notification envoyée à {employer.email} :\n{message}")

        if employer.email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [employer.email],
                fail_silently=True,
            )
