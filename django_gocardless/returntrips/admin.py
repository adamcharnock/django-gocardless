from django.contrib import admin
from .models import ReturnTrip

class ReturnTripAdmin(admin.ModelAdmin):
    list_display = ('status', 'for_model_class', 'for_pk', 'created')

    def has_add_permission(self, request):
        return False

admin.site.register(ReturnTrip, ReturnTripAdmin)

