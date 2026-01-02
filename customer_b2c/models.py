from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

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

class EXample(models.Model):
    temp_check = models.BooleanField(default=False)
