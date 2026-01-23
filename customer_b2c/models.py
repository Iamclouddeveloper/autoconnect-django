from django.conf import settings
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.exceptions import ValidationError
from datetime import date

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('sub_admin', 'Sub Admin'),
        ('user', 'User'),
    )
 
    username = models.CharField(max_length=150)

   
    email = models.EmailField(unique=True, max_length=191)

    # Optional profile photo
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='user'
    )

    is_blocked = models.BooleanField(default=False)
    pending_email = models.EmailField(null=True, blank=True)


    # Use email as the login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'user_tbl'

    def __str__(self):
        return self.email
    
class Vehicle(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )
    vrn = models.CharField(max_length=20)
    make = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mot_status = models.CharField(max_length=20, blank=True, null=True)
    mot_expiry_date = models.DateField(blank=True, null=True)

    tax_status = models.CharField(max_length=20, blank=True, null=True)
    tax_due_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    api_error = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'vehicle_registration'
        unique_together = ('user', 'vrn')

    def __str__(self):
        return f"{self.vrn} - {self.make} {self.model}"



class EmailQueue(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    to_email = models.EmailField()
    subject = models.CharField(max_length=200)

    template_name = models.CharField(
        max_length=100,
        help_text="Django template path"
    )

    context = models.JSONField(
        help_text="Template variables"
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )

    error = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'email_queue'
        ordering = ['created_at']
        
        
class Trip(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="trips"
    )

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,  
        related_name="trips"
    )

    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255, blank=True)

    estimated_distance  = models.FloatField(default=0,help_text="Estimated distance from map (miles)")
    actual_distance = models.FloatField(
        null=True,
        blank=True,
        help_text="Actual driven distance from odometer (miles)"
    )
    duration_text = models.CharField(max_length=100, blank=True)

    odometer_start = models.FloatField()
    odometer_end = models.FloatField(null=True, blank=True)

    latest_reading = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    tracking_token = models.CharField(max_length=40, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):
        if not self.tracking_token:
            self.tracking_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.start}"
    
    
    
class Driver(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    driver_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()

    contact_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='drivers_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'driver'
        ordering = ['-created_at']

    def clean(self):
        # Driver must be at least 17 years old
        today = date.today()
        age = today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )
        if age < 17:
            raise ValidationError("Driver must be at least 17 years old.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Licence(models.Model):
    licence_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    driver = models.OneToOneField(
        Driver,
        on_delete=models.CASCADE,
        related_name='licence'
    )

    licence_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    issuing_authority = models.CharField(
        max_length=50,
        default='DVLA'
    )


    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='licences_created'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'licence'

    def clean(self):
        if self.expiry_date <= date.today():
            raise ValidationError("Licence expiry date must be in the future.")

    def __str__(self):
        return self.licence_number
    
    
class LicenceCategory(models.Model):
    DVLA_CATEGORIES = (
        ('AM', 'AM'),
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('A', 'A'),
        ('B', 'B'),
        ('BE', 'BE'),
        ('C1', 'C1'),
        ('C1E', 'C1E'),
        ('C', 'C'),
        ('CE', 'CE'),
        ('D1', 'D1'),
        ('D1E', 'D1E'),
        ('D', 'D'),
        ('DE', 'DE'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    licence = models.ForeignKey(
        Licence,
        on_delete=models.CASCADE,
        related_name='categories'
    )

    category_code = models.CharField(
        max_length=5,
        choices=DVLA_CATEGORIES
    )

    class Meta:
        db_table = 'licence_category'
        unique_together = ('licence', 'category_code')

    def __str__(self):
        return self.category_code




class AuditLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=255)

    action = models.CharField(max_length=10, choices=ACTION_CHOICES)

    field_name = models.CharField(max_length=100, null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    # USER ID STORED HERE
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    performed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "audit_log"
        ordering = ["-performed_at"]

    def __str__(self):
        return f"{self.model_name} {self.action}"


class EXample(models.Model):
    temp_check = models.BooleanField(default=False)
