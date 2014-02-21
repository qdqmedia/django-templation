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

Edit `hello-templation/hellotemplation/core/models.py`

.. code-block:: python

    from django.db import models


    class Theme(models.Model):
        name = models.CharField(max_length=50, unique=True)


Edit `hello-templation/hellotemplation/core/views.py`

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
                return None

Edit `hello-templation/hellotemplation/hellotemplation/urls.py`

.. code-block:: python

    from django.conf.urls import patterns, include, url

    from django.contrib import admin
    admin.autodiscover()

    from core.views import Index

    urlpatterns = patterns('',
        url(r'^$', Index.as_view(), name='index'),
        url(r'^admin/', include(admin.site.urls)),
    )


Create index template (`hello-templation/hellotemplation/core/templates/core/index.html`)

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
        'core',  # Add your new app
    )
    ...

    # Django-templation settings
    TEMPLATION_DAV_ROOT = os.path.join(BASE_DIR, '..', 'dav')  # Make sure you create this folder
    TEMPLATION_DAV_STATIC_URL = '/templation_static/'
    TEMPLATION_RESOURCE_MODEL = 'core.models.Theme'

Launch for the first time

.. code-block:: bash

    $ python manage.py syncdb
    $ python manage.py runserver

Go to `http://127.0.0.1:8000`_ and you will see the `Hello world!`.

.. _http://127.0.0.1:8000: http://127.0.0.1:8000
