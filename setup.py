#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import templation

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def parse_requirements(requirements):
    with open(requirements) as f:
        return [l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')]

requirements_file = 'requirements.txt'
install_reqs = parse_requirements(os.path.abspath(os.path.join(os.path.dirname(__file__), requirements_file)))

version = templation.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-templation',
    version=version,
    description="""The easy way to allow designers edit templates and assets.""",
    long_description=readme + '\n\n' + history,
    author='QDQ media S.A.U.',
    author_email='tecnologia@qdqmedia.com',
    url='https://github.com/qdqmedia/django-templation',
    packages=[
        'templation',
    ],
    include_package_data=True,
    install_requires=install_reqs,
    license="BSD",
    zip_safe=False,
    keywords='django-templation',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)