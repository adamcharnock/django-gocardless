from django.contrib import admin
from .models import PartnerMerchant

class PartnerMerchantAdmin(admin.ModelAdmin):
    list_display = ('user', 'merchant_id', 'status')

admin.site.register(PartnerMerchant, PartnerMerchantAdmin)

