from django.contrib import admin
from .models import *

 
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Subscription)
admin.site.register(Users)
admin.site.register(Staff)
admin.site.register(Banking)
admin.site.register(Invoice)
admin.site.register(PaymentReceived)
admin.site.register(Vendors)
admin.site.register(Expenses)