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

    class Meta:
        db_table = 'vehicle_registration'
        unique_together = ('user', 'vrn')

    def __str__(self):
        return f"{self.vrn} - {self.make} {self.model}"
