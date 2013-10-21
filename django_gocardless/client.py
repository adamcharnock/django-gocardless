from django.conf import settings
import gocardless
from gocardless.client import Client

_client = None
def get_client():
    global _client
    if not _client:
        if settings.GOCARDLESS_SANDBOX:
            gocardless.environment = 'sandbox'
        _client = Client(
            app_id=settings.GOCARDLESS_APP_ID,
            app_secret=settings.GOCARDLESS_APP_SECRET,
            access_token=settings.GOCARDLESS_ACCESS_TOKEN,
            merchant_id=settings.GOCARDLESS_MERCHANT_ID,
        )
    return _client