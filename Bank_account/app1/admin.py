from django.contrib import admin
from app1.models import Bank, ATM, Operations, Clients

# Register your models here.
admin.site.register(Bank)
admin.site.register(ATM)
admin.site.register(Operations)
admin.site.register(Clients)
