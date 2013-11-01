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

_merchant_clients = {}
def get_merchant_client(merchant_id):
    global _merchant_clients
    merchant_id = str(merchant_id)
    if _merchant_clients.get(merchant_id):
        return _merchant_clients[merchant_id]
    else:
        if settings.GOCARDLESS_SANDBOX:
            gocardless.environment = 'sandbox'
        _client = Client(
            app_id=settings.GOCARDLESS_APP_ID,
            app_secret=settings.GOCARDLESS_APP_SECRET,
            access_token=settings.GOCARDLESS_ACCESS_TOKEN,
            merchant_id=merchant_id,
        )
        if settings.DEBUG:
            # Allows us to mock out the client in our
            # tests (as this will always return the same
            # instance for a given merchant).
            _merchant_clients[merchant_id] = _client
        return _client
