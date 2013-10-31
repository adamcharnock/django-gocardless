from django.conf.urls import patterns, include, url

from .views import partner_depart_view

urlpatterns = patterns('',
    url(r'^partner/depart/', partner_depart_view, name='gocardless_partner_depart'),
)