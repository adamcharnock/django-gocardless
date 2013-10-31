#!/usr/bin/env python
import sys
from os.path import dirname, abspath
from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        USE_TZ=True,
        GOCARDLESS_APP_ID='abcdefghijlmnopqrstuvwxyzabcdefghijlmnopqrstuvwxyz',
        GOCARDLESS_ACCESS_TOKEN='01234567890aaaaaaaaaaaaaaa',
        GOCARDLESS_MERCHANT_ID='123456',
        GOCARDLESS_APP_SECRET=(
            'BBYKKNKEK4WKN9YVK0BRARGS4QHDRVJB8J'
            'WYM84XTR9XQ591RGFSEFQ82B0ZKKYM'),
        ROOT_URLCONF='django_gocardless.urls',
        GOCARDLESS_SANDBOX=True,
        GOCARDLESS_RETURN_ROOT='https://example.com',
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django_gocardless.webhook',
            'django_gocardless.returntrips',
            'django_gocardless.preauthorizations',
            'django_gocardless.partner',
        ],
        NOSE_ARGS = [
            '--with-coverage',
            '--cover-package=django_gocardless',
            '--nocapture',
            '--logging-clear-handlers',
        ]
    )

parent = dirname(abspath(__file__))
sys.path.insert(0, parent)

from django_nose import NoseTestSuiteRunner
test_runner = NoseTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(sys.argv[1:] or ['django_gocardless', ])
if failures:
    sys.exit(failures)
