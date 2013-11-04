import django.dispatch

bill_paid = django.dispatch.Signal(providing_args=['bill', 'request'])