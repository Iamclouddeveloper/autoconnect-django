from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string

from customer_b2c.models import EmailQueue
class Command(BaseCommand):
    help = "Send queued emails"

    def handle(self, *args, **kwargs):
        emails = EmailQueue.objects.filter(status='pending')[:5]

        for item in emails:
            try:
                # Render the template using context
                html_body = render_to_string(item.template_name, item.context)

                msg = EmailMultiAlternatives(
                    subject=item.subject,
                    body="This email requires HTML support",
                    to=[item.to_email],
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()

                item.status = 'sent'
                item.sent_at = timezone.now()
                item.save()

            except Exception as e:
                item.status = 'failed'
                item.error = str(e)
                item.save()
