#!/usr/bin/env python
import os
import sys
import shutil

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
    try:
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'tests', 'media'))
    except OSError:
        # directory doesn't exist
        pass

    #
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == "__main__":
    main()
