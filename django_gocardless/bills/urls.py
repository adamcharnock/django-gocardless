from django.conf.urls import patterns, include, url

from .views import bill_depart_view

urlpatterns = patterns('',
    url(r'^bill/depart/', bill_depart_view, name='gocardless_bill_depart'),
)