from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('django_gocardless.webhook.urls')),
    url(r'^', include('django_gocardless.returntrips.urls')),
    url(r'^', include('django_gocardless.partners.urls')),
)
