#!/usr/bin/env python
import os
import sys
import shutil

import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == "__main__":
    shutil.rmtree(os.path.join(os.path.dirname(__file__), 'tests', 'media'))

    #
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
