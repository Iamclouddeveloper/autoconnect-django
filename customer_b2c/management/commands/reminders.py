from django.core.management.base import BaseCommand
from datetime import date, timedelta
from customer_b2c.models import Vehicle, EmailQueue

REMINDER_DAYS = [28, 21, 14, 7, 3, 2, 1]

EMAIL_TEMPLATE = 'vehicle_reminder_email.html'

class Command(BaseCommand):
    help = "Queue vehicle reminders"

    def handle(self, *args, **kwargs):
        today = date.today()
        vehicles = Vehicle.objects.select_related('user')

        for vehicle in vehicles:
            for days in REMINDER_DAYS:
                target_date = today + timedelta(days=days)

                if vehicle.mot_expiry_date == target_date:
                    self.queue(vehicle, 'MOT', vehicle.mot_expiry_date)

                if vehicle.tax_due_date == target_date:
                    self.queue(vehicle, 'TAX', vehicle.tax_due_date)

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
