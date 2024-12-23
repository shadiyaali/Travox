from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    
class Admin(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
 
    def __str__(self):
        return self.username


class Subscription(models.Model):
 
    plan_name = models.CharField(max_length=100, unique=True) 
    duration = models.PositiveIntegerField(help_text="Duration in months")

    def __str__(self):
        return f"{self.plan_name} ({self.duration} months)"
    
class Users(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ] 
    username = models.CharField(max_length=255, unique=True, null=True) 
    company_name = models.CharField(max_length=255)
    company_name_arabic = models.CharField(max_length=255, blank=True, null=True)
    company_location = models.CharField(max_length=255)
    number_of_branches = models.IntegerField()
    contact_numbers = models.CharField(max_length=255)
    company_email = models.EmailField()
    admin_email = models.EmailField()
    contact_person_name = models.CharField(max_length=255)
    company_address = models.TextField()
    gst_or_vat_required = models.CharField(max_length=20, choices=[('Yes', 'Yes'), ('No', 'No'), ('Maybe Later', 'Maybe Later')])
    gst_or_vat_number = models.CharField(max_length=255, blank=True, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    domain_name = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    default_services = models.CharField(
        max_length=255,
        choices=[
            ('Air Ticketing', 'Air Ticketing'),
            ('Visa Services', 'Visa Services'),
            ('Insurance', 'Insurance'),
            ('Emigration', 'Emigration'),
            ('Attestation', 'Attestation'),
            ('Holiday Packages', 'Holiday Packages'),
            ('Hotel Booking', 'Hotel Booking'),
            ('Train Tickets', 'Train Tickets'),
            ('Other', 'Other'),
        ]
    )
    other_service_details = models.CharField(max_length=255, blank=True, null=True)
 
    bank_account_details = models.TextField()
    bank_qr_code = models.ImageField(upload_to='bank_qr_codes/', blank=True, null=True)
    
    
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    accounts_auditing_needed = models.CharField(
        max_length=20,
        choices=[('Yes', 'Yes'), ('No', 'No'), ('Maybe in future', 'Maybe in future')]
    )
    invoice_excel_upload_option = models.CharField(max_length=20, choices=[('Yes', 'Yes'), ('No', 'No')])

    reference = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name
    
class Staff(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email  = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    date_joined = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    staff_role = models.CharField(
        max_length=255,
        choices=[
            ('Sales Staff', 'Sales Staff'),
            ('Accountant', 'Accountant'),
            
        ]
    )
 
    def __str__(self):
        return self.username
    