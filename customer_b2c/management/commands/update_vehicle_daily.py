import time
import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now

from customer_b2c.models import Vehicle
from customer_b2c.views import parse_date, calculate_first_mot_due
from customer_b2c.views import get_access_token


RATE_LIMIT_DELAY = 0.12  # ~8–10 req/sec


class Command(BaseCommand):
    help = "Daily MOT & TAX auto update"

    def handle(self, *args, **kwargs):
        vehicles = Vehicle.objects.filter(is_active=True)

        token = get_access_token()
        today = date.today()

        for vehicle in vehicles:
            vrn = vehicle.vrn

            try:
                # ---------- DVSA ----------
                dvsa_url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{vrn}"
                dvsa_headers = {
                    "Authorization": f"Bearer {token}",
                    "X-API-Key": settings.DVSA_API_KEY,
                    "Accept": "application/json"
                }

                dvsa_resp = requests.get(dvsa_url, headers=dvsa_headers, timeout=10)

                if dvsa_resp.status_code == 404:
                    vehicle.is_active = False
                    vehicle.api_error = "VRN invalid / removed"
                    vehicle.save(update_fields=["is_active", "api_error"])
                    continue

                dvsa_resp.raise_for_status()
                dvsa_data = dvsa_resp.json()
                reg_date = parse_date(dvsa_data.get("registrationDate"))

                time.sleep(RATE_LIMIT_DELAY)

                # ---------- DVLA ----------
                dvla_resp = requests.post(
                    "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles",
                    headers={
                        "x-api-key": settings.VRN_API_KEY,
                        "Content-Type": "application/json"
                    },
                    json={"registrationNumber": vrn},
                    timeout=10
                )

                dvla_resp.raise_for_status()
                dvla = dvla_resp.json()

                # ---------- Logic ----------
                if reg_date:
                    first_mot_due = calculate_first_mot_due(reg_date)
                    if today < first_mot_due:
                        mot_status = "No MOT required"
                        mot_expiry = first_mot_due
                    else:
                        mot_status = dvla.get("motStatus")
                        mot_expiry = parse_date(dvla.get("motExpiryDate"))
                else:
                    mot_status = dvla.get("motStatus")
                    mot_expiry = parse_date(dvla.get("motExpiryDate"))

                tax_status = dvla.get("taxStatus")
                tax_due = parse_date(dvla.get("taxDueDate"))

                # ---------- Update only if changed ----------
                changed = False

                if vehicle.mot_status != mot_status:
                    vehicle.mot_status = mot_status
                    changed = True

                if vehicle.mot_expiry_date != mot_expiry:
                    vehicle.mot_expiry_date = mot_expiry
                    changed = True

                if vehicle.tax_status != tax_status:
                    vehicle.tax_status = tax_status
                    changed = True

                if vehicle.tax_due_date != tax_due:
                    vehicle.tax_due_date = tax_due
                    changed = True

                vehicle.last_checked_at = now()
                vehicle.api_error = None

                vehicle.save()

                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                vehicle.api_error = str(e)
                vehicle.save(update_fields=["api_error"])
                continue

        self.stdout.write(self.style.SUCCESS("Vehicle update completed"))
