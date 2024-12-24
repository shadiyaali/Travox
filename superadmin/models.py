from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
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


from django.db import models

class Subscription(models.Model):
    plan_name = models.CharField(max_length=100, unique=True)
    duration = models.PositiveIntegerField(help_text="Duration in months")
    rate = models.IntegerField(default=True)

    def __str__(self):
        return f"{self.plan_name} ({self.duration} months, Rate: {self.rate})"

    
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
    
    
class Banking(models.Model):
    account_number = models.CharField(max_length=20, unique=True )
    account_holder_name = models.CharField(max_length=100 ,blank=True, null=True)
    bank_name = models.CharField(max_length=100 ,blank=True, null=True)
    branch_name = models.CharField(max_length=100 ,blank=True, null=True)
    ifsc_code = models.CharField(max_length=11,blank=True, null=True )

    def __str__(self):
        return f"{self.account_holder_name} - {self.bank_name}"
    
    
class Invoice(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partially paid','Partially Paid')
    ]
    customer_name = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_number = models.CharField(max_length=11, blank=True, null=True)
    invoice_date = models.DateField()
    terms = models.CharField(max_length=255, choices=[('Next 15', 'Next 15'), ('Next 30', 'Next 30'), ('Due on Receipt', 'Due on Receipt'), ('Due end of the month', 'Due end of the month')])
    due_date = models.DateField()
    sales_person = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    quotation_no = models.CharField(max_length=11, blank=True, null=True)
    lpo_number =models.CharField(max_length=11, blank=True, null=True)
    lpo_date = models.DateField(blank=True, null=True)
    subject = models.TextField()
    item = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.IntegerField(default=True)  
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Tax percentage (e.g., 15.25 for 15.25%)")
    notes = models.TextField(blank=True, null=True)
    discount = models.IntegerField(default=True) 
    total = models.IntegerField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='paid')

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.customer_name}"

    def clean(self):
        if self.sales_person and self.sales_person.staff_role != "Sales Staff":
            raise ValidationError({"sales_person": "The selected staff member is not a Sales Staff."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        

class PaymentReceived(models.Model):
    customer_name = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    amount_received = models.IntegerField(default=0)  
    payment_date = models.DateField()
    payment_mode = models.CharField(
        max_length=255, 
        choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('UPI', 'UPI')]
    )
    payment_number = models.CharField(max_length=11, blank=True, null=True)
    deposit_to = models.ForeignKey(Banking, on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField()
    invoice_no = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True)
    invoice_amount = models.IntegerField(default=0)  
    amount_due = models.IntegerField(default=0)  
    total = models.IntegerField(default=0)   

    def __str__(self):
        return f"Payment of {self.amount_received} for Invoice {self.invoice_no}"

    

class Vendors(models.Model):
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    phone_number = models.IntegerField()   
    opening_balance = models.IntegerField(default=0)   

    def __str__(self):
        return self.company_name

    
class Expenses(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('UPI', 'UPI'),
    ]

    EXPENSE_TYPE_CHOICES = [
        ('Goods', 'Goods'),
        ('Service', 'Service'),
    ]

    date = models.DateField()
    expense_account = models.CharField(max_length=255)
    amount =  models.IntegerField()
    paid_through = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES)
    expense_type = models.CharField(max_length=255, choices=EXPENSE_TYPE_CHOICES)
    vendor = models.ForeignKey(Vendors, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')

    class Meta:
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.expense_account} - {self.amount}"
