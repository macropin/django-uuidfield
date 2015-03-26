#!/usr/bin/env python
import sys
from django.conf import settings
from optparse import OptionParser

if not settings.configured:
    settings.configure(
        DATABASE_ENGINE='django.db.backends.postgresql_psycopg2',
        DATABASE_NAME='uuidfield_test',
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'uuidfield_test',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'uuidfield',
            'uuidfield.tests',
        ],
        ROOT_URLCONF='',
        DEBUG=False,
    )

from django_nose import NoseTestSuiteRunner


def runtests(*test_args, **kwargs):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['uuidfield']

    import django
    try:
        django.setup()
    except AttributeError:
        pass

    kwargs.setdefault('interactive', False)

    test_runner = NoseTestSuiteRunner(**kwargs)

    failures = test_runner.run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbosity', dest='verbosity', action='store', default=1, type=int)
    parser.add_options(NoseTestSuiteRunner.options)
    (options, args) = parser.parse_args()

    runtests(*args, **options.__dict__)
