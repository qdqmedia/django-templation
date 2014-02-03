import os
import sys

try:
    from django.conf import settings

    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.sessions",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "templation",
            "tests",
        ],
        SITE_ID=1,
        NOSE_ARGS=['-s'],

        TEMPLATION_DAV_ROOT='/tmp/dav/',
        TEMPLATION_RESOURCE_MODEL='tests.models.MyResource',
        RESOURCE_ACCESS_MODEL_INITIALIZER='tests.models.MyResource',
        TEMPLATION_REQUEST_RESOURCE_NAME='resource',

        STATICFILES_FINDERS=(
            'templation.finders.TemplationStaticFinder',
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
            # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
        ),

        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'templation.middleware.TemplationMiddleware',
        ),

        TEMPLATION_BOILERPLATE_FOLDER=os.path.join(BASE_DIR, 'tests', 'boilerplate')
    )

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
