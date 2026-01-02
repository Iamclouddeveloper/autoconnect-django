
from datetime import date, timedelta
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings

from .models import Vehicle, EmailQueue

REMINDER_DAYS = [28, 21, 14, 7, 3, 2, 1]

def queue_vehicle_reminders():
    today = date.today()

    vehicles = Vehicle.objects.select_related('user')

    for vehicle in vehicles:
        user = vehicle.user
        email = user.email

        for days in REMINDER_DAYS:
            target_date = today + timedelta(days=days)

            # MOT
            if vehicle.mot_expiry_date == target_date:
                _queue_email(vehicle, 'MOT', vehicle.mot_expiry_date)

            # TAX
            if vehicle.tax_due_date == target_date:
                _queue_email(vehicle, 'TAX', vehicle.tax_due_date)


def _queue_email(vehicle, reminder_type, expiry_date):
    context = {
        'username': vehicle.user.username,
        'vrn': vehicle.vrn,
        'reminder_type': reminder_type,
        'expiry_date': expiry_date,
       
    }

    html_body = render_to_string(
        'vehicle_reminder_email.html',
        context
    )

    EmailQueue.objects.create(
        user=vehicle.user,
        to_email=vehicle.user.email,
        subject=f"{reminder_type} Reminder – {vehicle.vrn}",
        body_html=html_body
    )
