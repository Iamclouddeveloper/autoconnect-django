import time
import requests
from datetime import date
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import now

from customer_b2c.models import Vehicle
from customer_b2c.views import parse_date, calculate_first_mot_due
from customer_b2c.views import get_access_token

import os
from datetime import datetime
from django.conf import settings
import json


BASE_DIR = os.path.join(settings.BASE_DIR, "logs")

LOG_BASE_DIR = os.path.join(settings.BASE_DIR, "logs", "vehicle_updates")

def write_json_log(entry: dict):
    os.makedirs(LOG_BASE_DIR, exist_ok=True)

    today_str = date.today().isoformat()
    log_file = os.path.join(LOG_BASE_DIR, f"{today_str}.json")

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


RATE_LIMIT_DELAY = 0.12  # ~8–10 req/sec

class Command(BaseCommand):
    help = "Daily MOT & TAX auto update"

    def handle(self, *args, **kwargs):
        log_message("auto_update.log", "Auto update command started")

        vehicles = Vehicle.objects.filter(is_active=True)
        today = date.today()

        try:
            token = get_access_token()
        except Exception as e:
            log_message("auto_update.log", f"FATAL: Token error | {e}")
            self.stderr.write("DVSA token error")
            return

        for vehicle in vehicles:
            vrn = vehicle.vrn

            dvsa_called = False
            dvla_called = False

            dvsa_remark = None
            dvla_remark = None

            old_mot_status = vehicle.mot_status
            old_mot_expiry = vehicle.mot_expiry_date
            old_tax_status = vehicle.tax_status
            old_tax_due = vehicle.tax_due_date

            log_message("auto_update.log", f"Processing vehicle VRN: {vrn}")

            try:
                # ---------- DVSA ----------
                dvsa_url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{vrn}"
                dvsa_headers = {
                    "Authorization": f"Bearer {token}",
                    "X-API-Key": settings.DVSA_API_KEY,
                    "Accept": "application/json"
                }

                dvsa_called = True
                dvsa_data = None

                try:
                    dvsa_resp = requests.get(dvsa_url, headers=dvsa_headers, timeout=10)

                    if dvsa_resp.status_code == 404:
                        dvsa_remark = "VRN invalid / removed (404)"
                    else:
                        dvsa_resp.raise_for_status()
                        dvsa_data = dvsa_resp.json()

                except requests.exceptions.HTTPError as e:
                    status = getattr(e.response, "status_code", "ERR")
                    reason = getattr(e.response, "reason", "HTTPError")
                    dvsa_remark = f"HTTP {status} {reason}"

                except requests.exceptions.RequestException:
                    dvsa_remark = "DVSA connection error"

                time.sleep(RATE_LIMIT_DELAY)

                # ---------- DVLA ----------
                dvla_called = True
                dvla = None

                try:
                    dvla_resp = requests.post(
                        "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles",
                        headers={
                            "x-api-key": settings.VRN_API_KEY,
                            "Content-Type": "application/json"
                        },
                        json={"registrationNumber": vrn},
                        timeout=10
                    )

                    if dvla_resp.status_code == 404:
                        dvla_remark = "VRN invalid / removed (404)"
                    else:
                        dvla_resp.raise_for_status()
                        dvla = dvla_resp.json()

                except requests.exceptions.HTTPError as e:
                    status = getattr(e.response, "status_code", "ERR")
                    reason = getattr(e.response, "reason", "HTTPError")
                    dvla_remark = f"HTTP {status} {reason}"

                except requests.exceptions.RequestException:
                    dvla_remark = "DVLA connection error"

                # ---------- INVALID VRN FLAG ----------
                invalid_vrn = (
                    dvsa_remark == "VRN invalid / removed (404)" or
                    dvla_remark == "VRN invalid / removed (404)"
                )

                # ---------- MOT / TAX UPDATE ----------
                mot_status = old_mot_status
                mot_expiry = old_mot_expiry
                tax_status = old_tax_status
                tax_due = old_tax_due

                if not invalid_vrn and dvla:
                    reg_date = parse_date(dvsa_data.get("registrationDate")) if dvsa_data else None

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

                    # Update vehicle only if data changed
                    if vehicle.mot_status != mot_status:
                        vehicle.mot_status = mot_status

                    if vehicle.mot_expiry_date != mot_expiry:
                        vehicle.mot_expiry_date = mot_expiry

                    if vehicle.tax_status != tax_status:
                        vehicle.tax_status = tax_status

                    if vehicle.tax_due_date != tax_due:
                        vehicle.tax_due_date = tax_due

                # ---------- CHANGE FLAGS ----------
                if invalid_vrn:
                    mot_changed = "N/A"
                    tax_changed = "N/A"
                else:
                    mot_changed = (
                        old_mot_status != vehicle.mot_status or
                        old_mot_expiry != vehicle.mot_expiry_date
                    )
                    tax_changed = (
                        old_tax_status != vehicle.tax_status or
                        old_tax_due != vehicle.tax_due_date
                    )

                vehicle.last_checked_at = now()
                vehicle.api_error = dvsa_remark or dvla_remark
                vehicle.save()

                # ---------- JSON LOG ----------
                log_data = {
                    "timestamp": datetime.now().isoformat(),
                    "vrn": vrn,
                    "dvsa_api_called": dvsa_called,
                    "dvla_api_called": dvla_called,
                    "mot_changes": {"changed": mot_changed},
                    "tax_changes": {"changed": tax_changed},
                    "remarks": {
                        "dvsa": dvsa_remark,
                        "dvla": dvla_remark,
                    }
                }

                # Include old/new only if changed=True
                if mot_changed is True:
                    log_data["mot_changes"].update({
                        "old_status": old_mot_status,
                        "new_status": vehicle.mot_status,
                        "old_expiry": old_mot_expiry,
                        "new_expiry": vehicle.mot_expiry_date,
                    })

                if tax_changed is True:
                    log_data["tax_changes"].update({
                        "old_status": old_tax_status,
                        "new_status": vehicle.tax_status,
                        "old_due": old_tax_due,
                        "new_due": vehicle.tax_due_date,
                    })

                write_json_log(log_data)
                time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                vehicle.api_error = str(e)[:90]
                vehicle.save(update_fields=["api_error"])

                write_json_log({
                    "timestamp": datetime.now().isoformat(),
                    "vrn": vrn,
                    "dvsa_api_called": dvsa_called,
                    "dvla_api_called": dvla_called,
                    "mot_changes": {"changed": False},
                    "tax_changes": {"changed": False},
                    "remarks": {
                        "dvsa": dvsa_remark,
                        "dvla": str(e),
                    }
                })

                log_message("auto_update.log", f"ERROR VRN {vrn} | {str(e)}")

        log_message("auto_update.log", "Auto update command finished")
        self.stdout.write(self.style.SUCCESS("Vehicle update completed"))
