from django.contrib import admin
from .models import *

 
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Subscription)
admin.site.register(Users)
admin.site.register(Staff)