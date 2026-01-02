# app/services/email_sender.py
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from .models import EmailQueue

def send_pending_emails(limit=5):
    emails = EmailQueue.objects.filter(status='pending')[:limit]

    for item in emails:
        try:
            msg = EmailMultiAlternatives(
                subject=item.subject,
                body="This email requires HTML support",
                to=[item.to_email],
            )
            msg.attach_alternative(item.body_html, "text/html")
            msg.send()

            item.status = 'sent'
            item.sent_at = timezone.now()
            item.save()

        except Exception as e:
            item.status = 'failed'
            item.error = str(e)
            item.save()
