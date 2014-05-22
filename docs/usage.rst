========
Usage
========

To use django-templation in a project


Django settings
------------------


Minimal Django configuration
++++++++++++++++++++++++++++

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


Settings in detail
++++++++++++++++++


TEMPLATION_DAV_ROOT
^^^^^^^^^^^^^^^^^^^

Default value: ``N/A``

Required: Yes

Defines the root path of *WebDAV* folder where designers will edit templates and static files.


TEMPLATION_DAV_STATIC_URL
^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``N/A``

Required: Yes

Defines the root url to access custom static files, it acts the same way as Django's ``STATIC_URL``, but only for ``django-templation``.


TEMPLATION_RESOURCE_MODEL
^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``N/A``

Required: Yes

The model that represents the *tenant*, templates will be bound to it.


TEMPLATION_PROVIDER_NAME
^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``'templation'``

Required: No

Provider name for WebDAV server. It also acts as the root url to access WebDAV folders.


TEMPLATION_BOILERPLATE_INITIALIZER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``'templation.models.copy_boilerplate_folder'``

Required: No

Path to a Python callable that will be executed when resource access object is created for the first time.


TEMPLATION_BOILERPLATE_FOLDER
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``None``

Required: No

Path to the folder containing the initial data for WebDAV shared folders.


TEMPLATION_DUMP_EXCEPTION
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``('TemplateDoesNotExist', 'TemplateSyntaxError')``

Required: No

Iterable of exception names that will be shown to the designers.


TEMPLATION_SECRET_KEY
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``SECRET_KEY``

Required: No

``SECRET_KEY`` used to generate access tokens.


TEMPLATION_SANDBOX
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``False``

Required: No

Activate sandbox environment for templates. Only whitelisted tags and filters will be available.


TEMPLATION_WHITELIST_TAGS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``DEFAULT_WHITELIST_TAGS``

Required: No

Safe template tags for sandbox.


TEMPLATION_WHITELIST_FILTERS
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``DEFAULT_WHITELIST_FILTERS``

Required: No

Safe template filters for sandbox.


TEMPLATION_EXTRA_LIBRARIES
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``DEFAULT_EXTRA_LIBRARIES``

Required: No

Preloaded tags and filters for sandbox.


TEMPLATION_DEBUG
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Default value: ``False``

Required: No

Activate templation's custom 500 error debug page.


DEFAULT_WHITELIST_TAGS
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    DEFAULT_WHITELIST_TAGS = [
        'comment', 'csrf_token', 'cycle', 'filter', 'firstof', 'for', 'if',
        'ifchanged', 'now', 'regroup', 'spaceless', 'templatetag', 'url',
        'widthratio', 'with', 'extends', 'include', 'block'
    ]


DEFAULT_WHITELIST_FILTERS
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    DEFAULT_WHITELIST_FILTERS = [
        'add', 'addslashes', 'capfirst', 'center', 'cut', 'date', 'default',
        'default_if_none', 'dictsort', 'dictsortreversed', 'divisibleby', 'escape',
        'escapejs', 'filesizeformat', 'first', 'fix_ampersands', 'floatformat',
        'force_escape', 'get_digit', 'iriencode', 'join', 'last', 'length', 'length_is',
        'linebreaks', 'linebreaksbr', 'linenumbers', 'ljust', 'lower', 'make_list',
        'phone2numeric', 'pluralize', 'pprint', 'random', 'removetags', 'rjust', 'safe',
        'safeseq', 'slice', 'slugify', 'stringformat', 'striptags', 'time', 'timesince',
        'timeuntil', 'title', 'truncatewords', 'truncatewords_html', 'unordered_list',
        'upper', 'urlencode', 'urlize', 'urlizetrunc', 'wordcount', 'wordwrap', 'yesno'
    ]


DEFAULT_EXTRA_LIBRARIES
```````````````````````

.. code-block:: python

    DEFAULT_EXTRA_LIBRARIES = [
        'templation.templatetags.templation_tags',
    ]


Enable WebDAV in your Django project
------------------------------------

`django-templation` uses `WsgiDAV`_ to expose WebDAV folders. To enable this functionality you must edit your `wsgi.py` file:

.. code-block:: python

    import os

    # We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
    # if running multiple sites in the same mod_wsgi process. To fix this, use
    # mod_wsgi daemon mode with each site in its own daemon process, or use
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")

    # This application object is used by any WSGI server configured to use this
    # file. This includes Django's development server, if the WSGI_APPLICATION
    # setting points here.
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    # Apply WSGI middleware here.
    # from helloworld.wsgi import HelloWorldApplication
    # application = HelloWorldApplication(application)

    from templation.middleware import WsgiDAVMiddleware
    application = WsgiDAVMiddleware(application)

.. _WsgiDAV: http://wsgidav.readthedocs.org/en/latest/



============================  ==========================================
 Required settings            Example value
============================  ==========================================
``TEMPLATION_DAV_ROOT``        ``/var/www/dav/``
``TEMPLATION_PROVIDER_NAME``   ``templation``
============================  ==========================================



Serving static content
-----------------------

``TEMPLATION_DAV_STATIC_URL`` defines the URL which serves customized statics. You need to
configure your web server (like NGINX) to serve this files properly


In this example ``TEMPLATION_DAV_STATIC_URL`` is set to ``/templationdav/``:

.. code-block :: nginx

    server {
        listen 80;

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


Static content in development mode
++++++++++++++++++++++++++++++++++

To serve templation's static content from development server (``python manage.py runserver``) it is necessary to add ``templation_static()`` to your url patterns
in your ``urls.py``:

.. code-block :: python

    from django.conf.urls import patterns, url, include
    from django.contrib import admin
    from templation.urls import templation_static  # Important line
    from .views import *

    admin.autodiscover()

    urlpatterns = patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^index/$', index, name='index'),
    ) + templation_static()  # Important line


Customizations
------------------

Resource Model
+++++++++++++++++++

The *Resource Model* can be any Django model.


Resource Access Model
++++++++++++++++++++++

*Resource Access Model* controls when 'development' templates and static files are shown. 
**Templation** comes with a default *Resource Access Model* but you can inherit from ``AbstractResourceAccess``
and make your custom one

.. code-block :: python

    from templation.models import AbstractResourceAccess, create_resource_access


    class CustomResourceAccess(AbstractResourceAccess):
        """ django-templation """

    post_save.connect(create_resource_access, sender=CustomResourceAccess)


Restricting template tags and filters
+++++++++++++++++++++++++++++++++++++++

You can set up a sandboxed environment for template designers restricting the use of builtin tags and filters
and preloading the desired ones.


In django settings:

.. code-block :: python

    TEMPLATION_SANDBOX = True  # Enables the sandbox mode

    # List of allowed tags
    TEMPLATION_WHITELIST_TAGS = [
        'comment', 'csrf_token', 'cycle', 'filter', 'firstof', 'for', 'if',
        'ifchanged', 'now', 'regroup', 'spaceless', 'templatetag', 'url',
        'widthratio', 'with', 'extends', 'include', 'block'
    ]

    # List of allowed filters
    TEMPLATION_WHITELIST_FILTERS = [
        'add', 'addslashes', 'capfirst', 'center', 'cut', 'date', 'default',
        'default_if_none', 'dictsort', 'dictsortreversed', 'divisibleby', 'escape',
        'escapejs', 'filesizeformat', 'first', 'fix_ampersands', 'floatformat',
        'force_escape', 'get_digit', 'iriencode', 'join', 'last', 'length', 'length_is',
        'linebreaks', 'linebreaksbr', 'linenumbers', 'ljust', 'lower', 'make_list',
        'phone2numeric', 'pluralize', 'pprint', 'random', 'removetags', 'rjust', 'safe',
        'safeseq', 'slice', 'slugify', 'stringformat', 'striptags', 'time', 'timesince',
        'timeuntil', 'title', 'truncatewords', 'truncatewords_html', 'unordered_list',
        'upper', 'urlencode', 'urlize', 'urlizetrunc', 'wordcount', 'wordwrap', 'yesno'
    ]

    # Preloaded tags
    TEMPLATION_EXTRA_LIBRARIES = [
        'yourapp.templatetags.yourapp_tags',
    ]


Debug 500 errors for designers
++++++++++++++++++++++++++++++

Designers may be overwhelmed by django's default 500 error page in debug mode, so `django-templation` includes
a custom 500 error view that shows debug information for the exceptions defined in ``TEMPLATION_DUMP_EXCEPTION`` setting.

To activate this functionality you have to add these lines to your ``urls.py``


.. code-block:: python

    from django.conf.urls import *
    handler500 = 'templation.views.server_error'


===========================  ==========================================
 Required settings           Example value
===========================  ==========================================
``TEMPLATION_DEBUG``         ``True``
===========================  ==========================================


.. _visibility:

Visibility of custom templates
------------------------------

The ``ResourceAccess`` (`RA`) object defines if a user can access a *WebDAV* folder associated with a object of class
``TEMPLATION_RESOURCE_MODEL``.

``ResourceAccess`` has two interesting properties:

- ``resource_pointer`` foreign key: Accesses the resource properties, where you have ``is_validated`` field, that indicates if the customized resources will be available for everyone.
- ``get_access_token()`` method: Returns an access token that allows everyone to see the customized version for this resource.


.. note:: You can also get the access token in the admin detail view of ``ResourceAccess`` object.


Table defining whether or not the customized template will be shown:

=============================  ======  ===================  ===============  =================
User type                      No RA   RA (not validated)   RA (validated)   Access token
=============================  ======  ===================  ===============  =================
User with ``ResourceAccess``   No      Yes                  Yes              Yes
Others                         No      No                   Yes              Yes
=============================  ======  ===================  ===============  =================

Extra goodies
-------------

``templation_tags.is_trusted_request`` is a template tags which tells whether a request comes from a trusted source. (an
ip address listed in ``settings.INTERNAL_IPS`` or an active, staff user). This can be used to show further debugging
information in the template being rendered.

`django-templation` comes with a custom context processor and a template tag which will help showing this additional
information to the designer.

The ``context_processor.templation_info`` context processor pushes two new variables into the templates context.
Together with the `Django admin documentation generator`_, you can point designers to documentation which is relevant to
the page they're working on.

===========================  ==========================================
 Variable name               Example value
===========================  ==========================================
``templation_view``          ``app.views.ItemList``
``templation_template``      ``item_list.html``
===========================  ==========================================


``templation_tags.get_model_info`` can additionally be used to link to models documentation in the
`Django admin documentation generator`_.

This is an example template block showcasing the integration that can be achieved:

.. code-block:: django

    {% load templation_tags %}

    {% if is_trusted_request %}
    <div>
        {% if object %}
            {% get_model_info object as model_info %}
        {% elif object_list %}
            {% get_model_info object_list as model_info %}
        {% endif %}

        <a href="{% url "django-admindocs-docroot" %}">Documentation</a> -
        <strong>Model:</strong>
            <a href="{% url 'django-admindocs-models-detail' app_label=model_info.app_label model_name=model_info.model_name %}">{{ model_info.model_name|capfirst }}</a> -
        <strong>View:</strong>
            <a href="{% url 'django-admindocs-views-detail' templation_view %}">{{ templation_view }}</a>
        <strong>Template:</strong>
            {{ templation_template }}
    </div>
    {% endif %}

.. _Django admin documentation generator: https://docs.djangoproject.com/en/dev/ref/contrib/admin/admindocs/