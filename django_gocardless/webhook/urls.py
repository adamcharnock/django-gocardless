from django.conf.urls import patterns, url

from .views import webhook_view

urlpatterns = patterns(
    '',
    url(r'^webhook/$', webhook_view, name="gocardless_webhook"),
)
