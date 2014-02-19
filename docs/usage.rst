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
    ]

    TEMPLATE_LOADERS = (
        'templation.loaders.TemplationLoader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader'
    )

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'templation.middleware.TemplationMiddleware',
    )

    TEMPLATION_BOILERPLATE_FOLDER = '/path/to/boilerplate/folder/'
    TEMPLATION_DAV_ROOT = '/path/to/webdav/folder/'
    TEMPLATION_DAV_STATIC_URL = '/templationdav/'  # URL to bind templation statics
    TEMPLATION_RESOURCE_MODEL = 'yourapp.models.MyResource'
    TEMPLATION_RESOURCE_ACCESS_MODEL = 'yourapp.models.CustomResourceAccessModel'  # OPTIONAL


Serving static content
-----------------------

`TEMPLATION_DAV_STATIC_URL` defines the URL which serves customized statics. You need to
configure your web server (like NGINX) to serve this files properly

.. code-block :: nginx

    server {
        listen 8080;

        location ~ ^/templationdav/(\d+)/(.*)$ {
            alias /your/davroot/$1/static/$2;
        }

        location /static/ {
            alias /your/static/path/;
        }

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:3031;
            uwsgi_param    SCRIPT_NAME '';
        }
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


Restricting template tags and filters
+++++++++++++++++++++++++++++++++++++++

You can set up a sandboxed environment for template designers restricting the use of builtin tags and filters
and preloading the desired ones.

TODO: write this well
