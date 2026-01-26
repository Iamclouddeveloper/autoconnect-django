from django.core.management.base import BaseCommand
from datetime import date, timedelta
from customer_b2c.models import Vehicle, EmailQueue
import os
from datetime import datetime
from django.conf import settings


BASE_DIR = os.path.join(settings.BASE_DIR, "logs")

def log_message(filename, message):
    os.makedirs(BASE_DIR, exist_ok=True)

    log_file = os.path.join(BASE_DIR, filename)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
        

REMINDER_DAYS = [28, 21, 14, 7, 3, 2, 1]

EMAIL_TEMPLATE = 'vehicle_reminder_email.html'

class Command(BaseCommand):
    help = "Queue vehicle reminders"

    def handle(self, *args, **kwargs):
        log_message("reminders.log", "Reminders command started")
        today = date.today()
        vehicles = Vehicle.objects.select_related('user')

        for vehicle in vehicles:
            for days in REMINDER_DAYS:
                target_date = today + timedelta(days=days)

                if vehicle.mot_expiry_date == target_date:
                    self.queue(vehicle, 'MOT', vehicle.mot_expiry_date)

                if vehicle.tax_due_date == target_date:
                    self.queue(vehicle, 'TAX', vehicle.tax_due_date)
        log_message("reminders.log", "Reminders command finished successfully")

    def queue(self, vehicle, reminder_type, expiry_date):
        EmailQueue.objects.create(
            user=vehicle.user,
            to_email=vehicle.user.email,
            subject=f"{reminder_type} Reminder – {vehicle.vrn}",
            template_name=EMAIL_TEMPLATE,
            context={
                'username': vehicle.user.username,
                'vrn': vehicle.vrn,
                'reminder_type': reminder_type,
                'expiry_date': expiry_date.strftime('%b %d, %Y'),
            }
        )
        log_message(
            "reminders.log",
            f"Queued {reminder_type} reminder for {vehicle.vrn} ({expiry_date})"
        )
