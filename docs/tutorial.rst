========
Tutorial
========

Welcome to Templation's tutorial. In this document you will integrate `django-templation` in a sample project. Our project will be a
very simple hello world with the feature multiple themes.


Setting up the environment and project
--------------------------------------

First things first, we are going to create our development environment and the `hello world` project.


Create project directory

.. code-block:: bash

    $ mkdir hello-templation
    $ cd hello-templation

Create virtualenv

.. code-block:: bash

    $ mkvirtualenv hello-templation


Create requirements.txt file::

    # requirements.txt
    django==1.6
    django-templation


Install requirements

.. code-block:: bash

    $ pip install -r requirements.txt

Create a new Django project

.. code-block:: bash

    $ django-admin.py startproject hellotemplation
    $ cd hellotemplation
    $ django-admin.py startapp core

Edit ``hello-templation/hellotemplation/core/models.py``

.. code-block:: python

    from django.db import models


    class Theme(models.Model):
        name = models.CharField(max_length=50, unique=True)


Edit ``hello-templation/hellotemplation/core/views.py``

.. code-block:: python

    from django.views.generic import TemplateView
    from templation.views import ResourceStoreMixin
    from .models import Theme

    class Index(ResourceStoreMixin, TemplateView):
        template_name = "core/index.html"

        def get_templation_object(self, *args, **kwargs):
            try:
                return Theme.objects.get(name=kwargs.get('theme-name', ''))
            except Theme.DoesNotExist:
                return Theme.objects.first()

Edit ``hello-templation/hellotemplation/hellotemplation/urls.py``

.. code-block:: python

    from django.conf.urls import patterns, include, url

    from django.contrib import admin
    admin.autodiscover()

    from templation.urls import templation_static
    from core.views import Index

    urlpatterns = patterns('',
        url(r'^$', Index.as_view(), name='index'),
        url(r'^admin/', include(admin.site.urls)),
    ) + templation_static()


Create index template (``hello-templation/hellotemplation/core/templates/core/index.html``)

.. code-block:: html

    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Hello world!</title>
        </head>
        <body>
            <p>Hello world!</p>
        </body>
    </html>


Configure settings

.. code-block:: python

    ...
    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'templation'
        'core',  # Add your new app
    )
    ...

    TEMPLATE_LOADERS = (
        'templation.loaders.TemplationLoader',
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader'
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'templation.middleware.TemplationMiddleware',
    )

    # Django-templation settings
    TEMPLATION_DAV_ROOT = os.path.join(BASE_DIR, '..', 'dav')  # Make sure you create this folder
    TEMPLATION_DAV_STATIC_URL = '/static_templation/'
    TEMPLATION_RESOURCE_MODEL = 'core.models.Theme'

Launch for the first time

.. code-block:: bash

    $ python manage.py syncdb
    $ python manage.py runserver

Go to `http://127.0.0.1:8000`_ and you will see the `Hello world!`.

.. _http://127.0.0.1:8000: http://127.0.0.1:8000


Setting up WebDAV shared resources
----------------------------------

The first thing to do is to make sure you have created the root folder for the WebDAV service (the one defined in ``TEMPLATION_DAV_ROOT``):

.. code-block:: bash

    $ sudo mkdir <TEMPLATION_DAV_ROOT>
    $ sudo chown youruser.yourgroup <TEMPLATION_DAV_ROOT>

Edit `wsgi.py` file in your Django project to activate WsgiDav middleware:

.. code-block:: python

    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hellotemplation.settings")

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from templation.middleware import WsgiDAVMiddleware
    application = WsgiDAVMiddleware(application)


Add boilerplate template to settings
++++++++++++++++++++++++++++++++++++

When a user is linked to a resource by a ``ResourceAccess`` object a default template is copied to its WebDAV folder if 
we define ``TEMPLATION_BOILERPLATE_FOLDER`` setting.

Create boilerplate files (in this example this folder is located at the same level of ``TEMPLATION_DAV_ROOT``)::

    dav_boilerplate/
    dav_boilerplate/templates
    dav_boilerplate/templates/core
    dav_boilerplate/templates/core/index.html
    dav_boilerplate/static
    dav_boilerplate/static/css
    dav_boilerplate/static/css/main.css
    dav_boilerplate/static/js
    dav_boilerplate/static/js/main.js


Edit ``settings.py``

.. code-block:: python

    ...
    TEMPLATION_BOILERPLATE_FOLDER = os.path.join(BASE_DIR, '..', 'dav_boilerplate')
    ...


Create some themes
++++++++++++++++++

.. code-block:: bash

    $ python manage.py shell

.. code-block:: pycon

    >>> from core.models import Theme
    >>> Theme.objects.create(name='simple')
    <Theme: Theme object>
    >>> Theme.objects.create(name='red')
    <Theme: Theme object>


Create ResourceAccess
+++++++++++++++++++++

.. code-block:: bash

    $ python manage.py shell

.. code-block:: pycon

    >>> from templation.settings import get_resource_access_model
    >>> from django.contrib.auth import get_user_model
    >>> from core.models import Theme
    >>> get_resource_access_model().objects.create(user=get_user_model().objects.get(username='admin'), resource=Theme.objects.get(name='simple'))
    <ResourceAccess: ResourceAccess object>


Accessing WebDAV folder
+++++++++++++++++++++++

``http://127.0.0.1:8000/<TEMPLATION_PROVIDER_NAME>/<RESOURCE_PK>/``

`http://127.0.0.1:8000/templation/1/`_ 

.. _http://127.0.0.1:8000/templation/1/: http://

.. note:: 
    When accessing the above URL you will be asked for the user credentials corresponding to the user linked in the ``ResourceAccess`` object.
    There are several more ways to access and change a WebDAV folder, more info on `WsgiDAV docs`_.
    
    .. _WsgiDAV docs: http://wsgidav.readthedocs.org/en/latest/run-access.html


Overriding a template
---------------------

Now that the WebDAV environment is set up, the next step is to modify the template.


Edit ``dav/1/templates/core/index.html``:

.. code-block:: django

    {% load static from templation_tags %}
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Hello world!</title>
            <link rel="stylesheet" href="{% static 'css/main.css' %}">
        </head>
        <body>
            <h1>Hello overriden world!</h1>
        </body>
    </html>

Edit ``dav/1/static/css/main.css``:

.. code-block:: css

    h1 {
        color:#333333;
        font-family:serif;
        text-shadow: 4px 4px 2px rgba(150, 150, 150, 1);
    }

Go to `http://127.0.0.1:8000`_ and you will see a fancier `Hello world!`.

.. warning:: Not showing the fancy Hello World? Checkout :ref:`visibility` section.
