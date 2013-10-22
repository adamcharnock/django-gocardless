from django.contrib import admin
from .models import PreAuthorization

class PreAuthorizationAdmin(admin.ModelAdmin):
    list_display = ('status', 'max_amount', 'name', 'user', 'created')

    def has_add_permission(self, request):
        return False

admin.site.register(PreAuthorization, PreAuthorizationAdmin)

