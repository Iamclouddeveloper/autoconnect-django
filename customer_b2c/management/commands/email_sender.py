from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.template.loader import render_to_string

from customer_b2c.models import EmailQueue
import os
from datetime import datetime, date
from django.conf import settings
import json


BASE_DIR = os.path.join(settings.BASE_DIR, "logs")



JSON_LOG_DIR = os.path.join(settings.BASE_DIR, "logs", "email_events")

def write_json_log(entry: dict):
    os.makedirs(JSON_LOG_DIR, exist_ok=True)

    today_str = date.today().isoformat()
    log_file = os.path.join(JSON_LOG_DIR, f"{today_str}.json")

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(log_file, "w") as f:
        json.dump(data, f, indent=2, default=str)


def log_message(filename, message):
    os.makedirs(BASE_DIR, exist_ok=True)

    log_file = os.path.join(BASE_DIR, filename)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

class Command(BaseCommand):
    help = "Send queued emails"

    def handle(self, *args, **kwargs):
        log_message("send_reminder_emails.log", "Email sender command started")
        
        emails = EmailQueue.objects.filter(status='pending')[:5]
        
        if not emails:
            log_message("send_reminder_emails.log", "No pending emails found")
            
            write_json_log({
                "timestamp": datetime.now().isoformat(),
                "event": "email_send",
                "status": "no_pending",
                "processed_count": 0,
                "message": "No pending emails found"
            })


        for item in emails:
            ctx = item.context or {}
            vrn = ctx.get("vrn", "N/A")
            reminder_type = ctx.get("reminder_type", "N/A")
            expiry_date = ctx.get("expiry_date", "N/A")

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
                
                log_message(
                    "send_reminder_emails.log",
                    f"Email SENT | ID:{item.id} | To:{item.to_email} | "
                    f"VRN:{vrn} | Type:{reminder_type} | Expiry:{expiry_date}"
                )
                # ----- JSON LOG -----
                write_json_log({
                    "timestamp": datetime.now().isoformat(),
                    "event": "email_send",
                    "email_id": item.id,
                    "status": "sent",
                    "to": item.to_email,
                    "vrn": vrn,
                    "reminder_type": reminder_type,
                    "expiry_date": expiry_date,
                    "template": item.template_name
                })

            except Exception as e:
                item.status = 'failed'
                item.error = str(e)
                item.save()
                
                log_message(
                    "send_reminder_emails.log",
                    f"Email FAILED | ID:{item.id} | To:{item.to_email} | "
                    f"VRN:{vrn} | Type:{reminder_type} | Expiry:{expiry_date} | Error:{str(e)}"
                )
                
                # ----- JSON LOG -----
                write_json_log({
                    "timestamp": datetime.now().isoformat(),
                    "event": "email_send",
                    "email_id": item.id,
                    "status": "failed",
                    "to": item.to_email,
                    "vrn": vrn,
                    "reminder_type": reminder_type,
                    "expiry_date": expiry_date,
                    "template": item.template_name,
                    "error": str(e)
                })
        log_message("send_reminder_emails.log", "Email sender command finished")
