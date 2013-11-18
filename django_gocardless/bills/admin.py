from django.contrib import admin
from .models import Bill

class BillAdmin(admin.ModelAdmin):
    list_display = ('user', 'to_user', 'amount', 'status')

admin.site.register(Bill, BillAdmin)

