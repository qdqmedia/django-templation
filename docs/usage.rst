========
Usage
========

To use django-templation in a project::


Django settings
------------------


.. code-block :: python


    INSTALLED_APPS = [
        'templation.builtins',
        "django.contrib.sessions",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "templation",
    ],

    STATICFILES_FINDERS = (
        'templation.finders.TemplationStaticFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ),


    TEMPLATE_LOADERS = (
        'templation.loaders.TemplationLoader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader'
    ),

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'templation.middleware.TemplationMiddleware',
    ),

    TEMPLATION_BOILERPLATE_FOLDER = '/path/to/boilerplate/folder/',
    TEMPLATION_DAV_ROOT = '/path/to/webdav/folder/',
    TEMPLATION_DAV_STATIC_URL = '/templationdav/',  # URL to bind templation statics
    TEMPLATION_RESOURCE_MODEL = 'yourapp.models.MyResource',
    TEMPLATION_RESOURCE_ACCESS_MODEL = 'yourapp.models.CustomResourceAccessModel',  # OPTIONAL
    TEMPLATION_BUILTIN_LIBRARIES = {
        'django.template.defaultfilters': {
            'exclude': {
                'filters': ['pprint'],
            }
        },
        'django.template.defaulttags': {
            'exclude': {
                'tags': ['load']
            }
        },
        'django.template.loader_tags': {},
        'templation.templatetags.static': {},
    }


Customizations
------------------

Resource Model
+++++++++++++++++++

The *Resource Model* can be any Django model.


Resource Access Model
+++++++++++++++++++

*Resource Access Model* controls when 'development' templates and static files are shown. 
**Templation** comes with a default *Resource Access Model* but you can inherit from `AbstractResourceAccess` 
and make your custom one

.. code-block :: python

    from templation.models import AbstractResourceAccess


    class CustomResourceAccess(AbstractResourceAccess):
        """ django-templation """
