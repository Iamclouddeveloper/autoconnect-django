from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import json
import requests
from django.http import HttpResponse, JsonResponse
import re
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
import time
import pdfkit
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Vehicle
from django.core.mail import EmailMultiAlternatives
import random


 

User = get_user_model()


def index(request):
    # ---------- CAPTCHA GENERATION ----------
    if "captcha" not in request.session:
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        request.session["captcha"] = a + b
        request.session["captcha_q"] = f"{a} + {b}"

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        company = request.POST.get("company", "").strip()
        message_text = request.POST.get("message", "").strip()
        captcha_answer = request.POST.get("captcha_answer")

        
        if not name or not email or not message_text:
            messages.error(request, "All required fields must be filled.")
            return redirect("index")

        if not captcha_answer or int(captcha_answer) != request.session.get("captcha"):
            messages.error(request, "Incorrect security answer.")
            return redirect("index")

        # CAPTCHA passed → remove it
        request.session.pop("captcha", None)
        request.session.pop("captcha_q", None)

        # ---------- EMAIL TO ADMIN ----------
        admin_html = render_to_string('contact_email.html', {
            'name': name,
            'email': email,
            'company': company,
            'message': message_text
        })

        admin_email = EmailMultiAlternatives(
            subject='New Contact Message – AutoNgx',
            body='New contact enquiry received.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL], 
            cc=['mohamedriyas.py@gmail.com']  
        )
        admin_email.attach_alternative(admin_html, "text/html")
        admin_email.send()
        

        # ---------- AUTO REPLY TO USER ----------
        auto_html = render_to_string('auto_reply_email.html', {
            'name': name
        })

        auto_email = EmailMultiAlternatives(
            subject='Thank you for contacting AutoNgx',
            body='Thank you for contacting AutoNgx.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        auto_email.attach_alternative(auto_html, "text/html")
        auto_email.send()

        messages.success(request, "Thank you! Your message has been sent.")
        return redirect("index")

    # GET request
    return render(request, "index.html", {
        "captcha_question": request.session.get("captcha_q")
    })


# ---------------- REGISTER ----------------
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        

        # Check if user exists
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            if not existing_user.is_active:
                # Resend verification email with new token
                uid = urlsafe_base64_encode(force_bytes(existing_user.pk))
                token = default_token_generator.make_token(existing_user)
                verify_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

                html_content = render_to_string('verify_email_template.html', {
                    'username': existing_user.username,
                    'email': email,
                    'verify_link': verify_link
                })

                subject = 'Verify your AutoNgx email'
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = [email]

                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                messages.success(request, 'Verification email resent. Check your inbox.')
                return redirect('login')
            else:
                messages.error(request, 'Email already registered')
                return redirect('register')

        # Create new user if not exists
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False,
            role='user'
        )

        # Send verification email for new user
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')

        html_content = render_to_string('verify_email_template.html', {
            'username': username,
            'email': email,
            'verify_link': verify_link
        })

        subject = 'Verify your AutoNgx email'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, 'Verification email sent. Check your inbox.')
        return redirect('login')

    return render(request, 'registration.html')

# ---------------- VERIFY EMAIL ----------------
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email verified. You can login now.')
        return redirect('login')

    messages.error(request, 'Invalid or expired verification link')
    return redirect('register')


# ---------------- LOGIN ----------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email address')
            return redirect('login')
        
        if not user_obj.is_active:
            messages.error(request, 'Please verify your email')
            return redirect('login')
        
        if user_obj.is_blocked:
            messages.error(request, 'Your account is suspended')
            return redirect('login')
        
        if not user_obj.check_password(password):
            messages.error(request, 'Incorrect password')
            return redirect('login')
        
        

        user = authenticate(request, email=email, password=password)

        

        if user is None:
            messages.error(request, 'Login failed. Please try again.')
            return redirect('login')

        login(request, user)
        messages.success(request, 'Login successful. Welcome back!')

        # Role-based redirect
        if user.role in ['super_admin', 'sub_admin']:
            return redirect('admin_dashboard')
 
        
        return redirect('my_vehicle')  

    return render(request, 'login.html')


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':

        # ---------------- REMOVE PROFILE PHOTO ----------------
        if 'remove_photo' in request.POST:
            if user.profile_photo:
                user.profile_photo.delete(save=True)
                messages.success(request, 'Profile photo removed')
            return redirect('profile')

        has_error = False  

        # ---------------- USERNAME ----------------
        new_username = request.POST.get('username', '').strip()
        if new_username and new_username != user.username:
            user.username = new_username

        # ---------------- PASSWORD ----------------
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password:
            if password == confirm_password:
                user.set_password(password)
            else:
                messages.error(request, 'Passwords do not match!')
                has_error = True

        # ---------------- PROFILE PHOTO ----------------
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']

        # ---------------- EMAIL (VALIDATE FIRST) ----------------
        new_email = request.POST.get('email', '').strip()

        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email already exists!')
                has_error = True
            else:
                user.pending_email = new_email

        #  Do not save if there is any error
        if has_error:
            return redirect('profile')

        #  Save ONCE
        user.save()

        #  SEND EMAIL ONLY AFTER SAVE 
        if user.pending_email:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            verify_link = request.build_absolute_uri(
                f'/verify-email-change/{uid}/{token}/'
            )

            html_content = render_to_string('email_change_verification.html', {
                'username': user.username,
                'verify_link': verify_link,
            })

            subject = 'Verify your new email address'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [user.pending_email]

            # Create email message with HTML content
            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(
                request,
                'Verification email sent. Your email will update after verification.'
            )
        else:
            messages.success(request, 'Profile updated successfully.')

        update_session_auth_hash(request, user)
        return redirect('profile')

    return render(request, 'profile.html')


def verify_email_change(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if user.pending_email:
            user.email = user.pending_email
            user.pending_email = None
            user.save()
            messages.success(request, 'Email updated successfully!')
        else:
            messages.error(request, 'No email change request found.')
    else:
        messages.error(request, 'Invalid or expired verification link.')

    return redirect('profile')



# ---------------- LOGOUT ----------------
def logout_view(request):
    logout(request)
    return redirect('login')





class CustomPasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # This includes user.pk and password hash in token
        return f"{user.pk}{user.password}{timestamp}"

token_generator = CustomPasswordResetTokenGenerator()



def generate_reset_link(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)

    return request.build_absolute_uri(
        reverse('reset_password', kwargs={
            'uidb64': uid,
            'token': token
        })
    )

def send_reset_email(request, user):
    reset_link = generate_reset_link(request, user)
    html_content = render_to_string('password_reset_email_template.html', {
        'username': user.username,
        'reset_link': reset_link,
    })
    subject = 'Password Reset Request'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]


    msg = EmailMultiAlternatives(subject, '', from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def verify_reset_token(uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None

    if not token_generator.check_token(user, token):
        return None

    return user





def request_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            send_reset_email(request, user)
        except User.DoesNotExist:
            pass  # prevent email enumeration

        messages.info(request, 'If the email exists, a reset link has been sent.')
        return redirect('login')

    return render(request, 'request_reset.html')





def reset_password(request, uidb64, token):
    user = verify_reset_token(uidb64, token)

    if not user:
        messages.error(request, 'Invalid or expired reset link.')
        return redirect('login')

    if request.method == 'POST':
        password = request.POST.get('password')

        if len(password) < 8:
            messages.warning(request, 'Password must be at least 8 characters.')
            return render(request, 'reset_password.html')

        user.set_password(password)  # secure hashing
        user.save()
        messages.success(request, 'Password updated successfully.')
        return redirect('login')

    return render(request, 'reset_password.html')


# ---------------- search VRN  ----------------


# Define field orders for vehicle details and MOT history
VEHICLE_DETAILS_FIELD_ORDER = [
    "Registration Number", "Make", "Colour", "Fuel Type", "Year of Manufacture", "Engine Capacity",
    "Month of First Registration", "Mot Status", "Mot Expiry Date", "Tax Status", "Tax Due Date", "Euro Status",
    "Marked For Export", "Revenue Weight", "Co2 Emissions", "Date of Last V5C issued", "Type Approval", "Wheelplan"
]

def format_field_name(field_name):
    formatted_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', field_name)
    formatted_name = formatted_name.title()
    formatted_name = re.sub(r'\bOf\b', 'of', formatted_name)
    formatted_name = re.sub(r'\bCo2 Emissions\b', 'CO2 Emissions', formatted_name)
    formatted_name = re.sub(r'\bV5 C Issued\b', 'V5C issued', formatted_name)
    return formatted_name


def format_json_keys(data):
    formatted_data = {}

    for key, value in data.items():
        formatted_key = format_field_name(key)

        if isinstance(value, dict):
            formatted_data[formatted_key] = format_json_keys(value)

        elif isinstance(value, list):
            formatted_data[formatted_key] = [
                format_json_keys(item) if isinstance(item, dict) else item
                for item in value
            ]

        else:
            if isinstance(value, str):
                # YYYY-MM-DD → DD-MM-YYYY
                value = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3-\2-\1', value)
                # YYYY-MM → MM-YYYY
                value = re.sub(r'(\d{4})-(\d{2})$', r'\2-\1', value)

            formatted_data[formatted_key] = value

    
    ordered_data = {
        field: formatted_data.get(field, 'N/A')
        for field in VEHICLE_DETAILS_FIELD_ORDER
    }

    return ordered_data


@csrf_exempt
def search_vrn(request):
    if request.method == 'POST':
        
        
        try:
            data = json.loads(request.body)
            if not data or 'vrn' not in data:
                return JsonResponse(
                    {'error': 'Invalid VRN reference provided'},
                    status=400
                )

            vrn = data['vrn']

            headers = {
                'x-api-key': settings.VRN_API_KEY,
                'Content-Type': 'application/json',
            }

            payload = {
                "registrationNumber": vrn
            }

            api_url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()

            formatted_response = format_json_keys(response.json())
            ordered_data = {
                field: formatted_response.get(field, 'N/A')
                for field in VEHICLE_DETAILS_FIELD_ORDER
            }

            django_response = JsonResponse(ordered_data)
            django_response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            django_response['Pragma'] = 'no-cache'
            django_response['Expires'] = '0'
            return django_response

        except requests.RequestException as req_err:
            print(f'Request error occurred: {req_err}')
            return JsonResponse(
                {'error': 'VRN details not found, try again'},
                status=404
            )

        except Exception as err:
            print(f'An unexpected error occurred: {err}')
            return JsonResponse(
                {'error': 'An unexpected error occurred'},
                status=500
            )

    return render(request, 'search-vrn.html')


# ---------------- search MOT ----------------

def convert_date_format(date_str, include_time=False):
    if not date_str or date_str == 'N/A':
        return 'N/A'

    try:
        if include_time:
            # 2024-01-12T10:30:00.000Z → 12-01-2024 10:30
           
            dt = datetime.fromisoformat(date_str.replace('Z', ''))
            return dt.strftime('%d-%m-%Y %H:%M')
        else:
            # 2024-01-12 → 12-01-2024
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%d-%m-%Y')
    except Exception:
        return date_str


# Format all vehicle dates
def format_vehicle_dates(vehicle):
    vehicle['firstUsedDate'] = convert_date_format(vehicle.get('firstUsedDate'))
    vehicle['registrationDate'] = convert_date_format(vehicle.get('registrationDate'))
    vehicle['manufactureDate'] = convert_date_format(vehicle.get('manufactureDate'))
    return vehicle


# Format all MOT test dates
def format_mot_test_dates(record):
    record['completedDate'] = convert_date_format(
        record.get('completedDate'), include_time=True
    )
    record['expiryDate'] = convert_date_format(record.get('expiryDate'))
    return record


TOKEN_CACHE = {"token": None, "expiry": 0}

def get_access_token():
    if TOKEN_CACHE["token"] and time.time() < TOKEN_CACHE["expiry"] - 60:
        return TOKEN_CACHE["token"]

    data = {
        "grant_type": "client_credentials",
        "client_id": settings.DVSA_CLIENT_ID,
        "client_secret": settings.DVSA_CLIENT_SECRET,
        "scope": settings.DVSA_SCOPE,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    resp = requests.post(
        f"https://login.microsoftonline.com/{settings.DVSA_TENANT_ID}/oauth2/v2.0/token",
        data=data,
        headers=headers,
        timeout=10,
    )
    resp.raise_for_status()

    token_data = resp.json()
    TOKEN_CACHE["token"] = token_data["access_token"]
    TOKEN_CACHE["expiry"] = time.time() + token_data.get("expires_in", 3600)

    return TOKEN_CACHE["token"]


@csrf_exempt  
def search_mot(request):
    

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            vrn = data.get('vrn')

            if not vrn:
                return JsonResponse(
                    {'error': 'Vehicle Registration Number is required'},
                    status=400
                )

            token = get_access_token()

            url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{vrn.replace(' ', '')}"

            headers = {
                "Authorization": f"Bearer {token}",
                "X-API-Key": settings.DVSA_API_KEY,
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return JsonResponse({'error': 'No MOT data found'}, status=404)

            response.raise_for_status()

            json_data = response.json()

            # DVSA TAPI returns ONE vehicle object
            vehicle = json_data
            if request.user.is_authenticated:
                try:
                    db_vehicle = Vehicle.objects.get(user=request.user, vrn=vrn)
                    mot_expiry_date = db_vehicle.mot_expiry_date.strftime('%d-%m-%Y') if db_vehicle.mot_expiry_date else 'N/A'
                    tax_due_date = db_vehicle.tax_due_date.strftime('%d-%m-%Y') if db_vehicle.tax_due_date else 'N/A'
                except Vehicle.DoesNotExist:
                    mot_expiry_date = 'N/A'
                    tax_due_date = 'N/A'
            else:
                mot_expiry_date = 'N/A'
                tax_due_date = 'N/A'



            vehicle_details = {
                'registration': vehicle.get('registration', 'N/A'),
                'make': vehicle.get('make', 'N/A'),
                'model': vehicle.get('model', 'N/A'),
                'firstUsedDate': vehicle.get('firstUsedDate', 'N/A'),
                'fuelType': vehicle.get('fuelType', 'N/A'),
                'primaryColour': vehicle.get('primaryColour', 'N/A'),
                'engineSize': vehicle.get('engineSize', 'N/A'),
                'registrationDate': vehicle.get('registrationDate', 'N/A'),
                'manufactureDate': vehicle.get('manufactureDate', 'N/A'),
                'mot_expiry_date': mot_expiry_date,
                'tax_due_date': tax_due_date,
            }

            vehicle_details = format_vehicle_dates(vehicle_details)

            mot_tests = vehicle.get('motTests', [])
            if not mot_tests:
                return JsonResponse({
                    'vehicleDetails': vehicle_details,
                    'message': (
                        'MOT test reports and history are only available '
                        'for vehicles more than 3 years old.'
                    )
                })

            mot_records = []
            for record in mot_tests:
                mot_test_data = {
                    'completedDate': record.get('completedDate', 'N/A'),
                    'expiryDate': record.get('expiryDate', 'N/A'),
                    'odometerReading': record.get('odometerValue', 'N/A'),
                    'testResult': record.get('testResult', 'N/A'),
                    'motTestNumber': record.get('motTestNumber', 'N/A'),
                    'testNotes': [
                        note.get('text', 'N/A')
                         for note in record.get('defects', [])
                    ],
                }

                mot_test_data = format_mot_test_dates(mot_test_data)
                mot_records.append(mot_test_data)

            return JsonResponse({
                'vehicleDetails': vehicle_details,
                'motRecords': mot_records
            })

        except requests.exceptions.Timeout:
            return JsonResponse(
                {'error': 'MOT service timeout. Try again.'},
                status=504
            )

        except requests.exceptions.ConnectionError:
            return JsonResponse(
                {'error': 'MOT service unavailable'},
                status=503
            )

        except Exception as err:
            print(err)
            return JsonResponse(
                {'error': 'An unexpected error occurred'},
                status=500
            )

    return render(request, 'search-mot.html')




#  genarete mot pdf 




def generate_pdf(vehicle_details, mot_records, is_dashboard=False):
   
    vrn = vehicle_details.get('registration', 'UNKNOWN')
    current_time = datetime.now().strftime('%d-%b-%Y, %H:%M')
    vehicle_details['mot_expiry_date'] = vehicle_details.get('mot_expiry_date', 'N/A')
    vehicle_details['tax_due_date'] = vehicle_details.get('tax_due_date', 'N/A')


    rendered_html = render_to_string(
        'mot-history.html',
        {
            'vehicle_details': vehicle_details,
            'mot_records': mot_records,
            'report_time': current_time,
            'is_dashboard': is_dashboard 
        }
    )

    pdf_options = {
        'footer-center': (
            f'Vehicle MOT History Report | '
            f'Vehicle Registration Number: {vrn} | '
            f'Page [page] of [topage]'
        ),
        'footer-font-size': '6',
        'footer-spacing': '5',
        'margin-bottom': '15mm',
        'encoding': 'UTF-8'
    }

    pdf_output = pdfkit.from_string(
        rendered_html,
        False,
        configuration=settings.PDFKIT_CONFIG,
        options=pdf_options
    )

    return pdf_output





@csrf_exempt  # send CSRF token instead in production
def generate_pdf_endpoint(request):
   
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=405)

    try:
        data = json.loads(request.body)

        vrn = data.get('vrn')
        vehicle_details = data.get('vehicle_details')
        mot_records = data.get('motRecords', [])
        is_dashboard = data.get('isDashboard', False)

        if not vrn or not vehicle_details:
            return JsonResponse(
                {'error': 'Vehicle details not found'},
                status=404
            )
        vehicle_details['mot_expiry_date'] = vehicle_details.get('mot_expiry_date', 'N/A')
        vehicle_details['tax_due_date'] = vehicle_details.get('tax_due_date', 'N/A')

        pdf_output = generate_pdf(vehicle_details, mot_records,is_dashboard=is_dashboard)
        

        response = HttpResponse(
            pdf_output,
            content_type='application/pdf'
        )

        response['Content-Disposition'] = (
            f'attachment; filename="MOT_History_{vrn}.pdf"'
        )

        return response

    except Exception as e:
        print(e)
        return JsonResponse(
            {'error': 'PDF generation failed'},
            status=500
        )


# admin dashbord

@login_required
def admin_dashboard(request):

    # Only admin roles allowed
    if request.user.role not in ['super_admin', 'sub_admin']:
        return redirect('profile')

    # Super admin → all users
    if request.user.role == 'super_admin':
        users = User.objects.all().order_by('-date_joined')

    # Sub admin → exclude super_admin
    else:
        users = User.objects.exclude(role__in=['super_admin', 'sub_admin']).order_by('-date_joined')

    context = {
        'users': users
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
def toggle_block_user(request, user_id):

    if request.method != "POST":
        return redirect('admin_dashboard')

    # Only admins allowed
    if request.user.role not in ['super_admin', 'sub_admin']:
        messages.error(request, "Permission denied.")
        return redirect('profile')

    user = get_object_or_404(User, id=user_id)

    # Sub-admin cannot block super_admin
    if request.user.role == 'sub_admin' and user.role == 'super_admin':
        messages.error(request, "You cannot block a Super Admin.")
        return redirect('admin_dashboard')

    # Prevent blocking yourself
    if user == request.user:
        messages.error(request, "You cannot block yourself.")
        return redirect('admin_dashboard')

    user.is_blocked = not user.is_blocked
    user.save()

    messages.success(
        request,
        f"User {'blocked' if user.is_blocked else 'unblocked'} successfully."
    )

    return redirect('admin_dashboard')


@login_required
@require_POST
def delete_users(request):

    if request.user.role != 'super_admin':
        return JsonResponse({"error": "Permission denied"}, status=403)

    ids = request.POST.getlist("user_ids[]")

    if not ids:
        return JsonResponse({"error": "No users selected"}, status=400)

    users = User.objects.filter(id__in=ids)

    # Prevent deleting yourself
    if str(request.user.id) in ids:
        return JsonResponse({"error": "You cannot delete yourself"}, status=400)

    # Prevent deleting other super_admins
    protected = users.filter(role='super_admin')
    if protected.exists():
        return JsonResponse({"error": "Cannot delete Super Admin users"}, status=400)

    deleted_count = users.delete()[0]

    return JsonResponse({"success": True, "deleted": deleted_count})




@login_required
def update_user(request):
    if request.method == "POST" and request.user.role == "super_admin":
        user_id = request.POST.get("id")
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "").strip()

        #  VALIDATION
        if not username or not email:
            return JsonResponse({"error": "Username and email cannot be empty."}, status=400)
        if len(username) < 3 or len(username) > 15:
            return JsonResponse({"error": "Username must be between 3 and 15 characters."}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"error": "Invalid email format."}, status=400)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "User does not exist."}, status=404)

        # Save values
        user.username = username
        user.email = email
        user.role = role
        user.save()

        return JsonResponse({"success": True})

    return JsonResponse({"error": "unauthorized"}, status=403)


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date() if value else None

def calculate_first_mot_due(reg_date):
    try:
        third_anniversary = reg_date.replace(year=reg_date.year + 3)
    except ValueError:
        # Handles 29 Feb → 28 Feb
        third_anniversary = reg_date.replace(
            year=reg_date.year + 3,
            day=28
        )

    return third_anniversary - timedelta(days=1)


@login_required
def add_vehicle(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            vrn = data.get('vrn', '')
            vrn = vrn.strip().upper().replace(" ", "")

            if not vrn:
                return JsonResponse({'error': 'VRN required'}, status=400)

            if Vehicle.objects.filter(user=request.user, vrn=vrn).exists():
                return JsonResponse(
                    {'error': 'Vehicle already added'},
                    status=409
                )

            token = get_access_token()

            url = f"https://history.mot.api.gov.uk/v1/trade/vehicles/registration/{vrn}"

            headers = {
                "Authorization": f"Bearer {token}",
                "X-API-Key": settings.DVSA_API_KEY,
                "Accept": "application/json"
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 404:
                return JsonResponse({'error': 'Invalid VRN'}, status=404)

            response.raise_for_status()
            vehicle = response.json()
            registration_date = parse_date(vehicle.get("registrationDate"))
            
            # --- ADD THIS BLOCK (DVLA API call) ---
            dvla_url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

            dvla_headers = {
                "x-api-key": settings.VRN_API_KEY,
                "Content-Type": "application/json"
            }

            dvla_payload = {
                "registrationNumber": vrn
            }

            dvla_response = requests.post(
                dvla_url,
                headers=dvla_headers,
                json=dvla_payload,
                timeout=10
            )

            dvla_response.raise_for_status()
            dvla_data = dvla_response.json()
            
            today = date.today()
            #  New vehicle logic 
            if registration_date:
                first_mot_due = calculate_first_mot_due(registration_date)

                if today < first_mot_due:
                    mot_status = "No MOT required"
                    mot_expiry = first_mot_due
                else:
                    mot_status = dvla_data.get("motStatus") or "Not valid"
                    mot_expiry = parse_date(dvla_data.get("motExpiryDate"))
            else:
                mot_status = dvla_data.get("motStatus") or "Not valid"
                mot_expiry = parse_date(dvla_data.get("motExpiryDate"))
           

            tax_status = dvla_data.get("taxStatus")
            tax_due = parse_date(dvla_data.get("taxDueDate"))
            # --- Insert values---


            Vehicle.objects.create(
                user=request.user,
                vrn=vrn,
                make=vehicle.get('make', ''),
                model=vehicle.get('model', ''),
                
                mot_status=mot_status,
                mot_expiry_date=mot_expiry,
                tax_status=tax_status,
                tax_due_date=tax_due
            )

            return JsonResponse(
                {'message': f'{vrn} added successfully'},
                status=201
            )

        except requests.exceptions.RequestException:
            return JsonResponse(
                {'error': 'Vehicle service unavailable'},
                status=503
            )

        except Exception as e:
            print(e)
            return JsonResponse(
                {'error': 'Unexpected error'},
                status=500
            )

    return render(request, 'add-vehicle.html')


@login_required()
def my_vehicle(request):
    vehicles = Vehicle.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my-vehicle.html', {'vehicles': vehicles})


@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    vehicle.delete()
    messages.success(request, "Vehicle deleted successfully")
    return redirect('my_vehicle')


