from django.conf.urls import patterns, url
from .views import return_view


urlpatterns = patterns(
    '',
    url(r'^redirect-return/$', return_view, name="gocardless_redirect_return"),
)
