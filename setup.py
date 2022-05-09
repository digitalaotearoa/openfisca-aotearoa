#! /usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


setup(
    name='OpenFisca-Aotearoa',
    version='12.0.0',
    author='New Zealand Government, Service Innovation Lab',
    author_email='brenda.wallace@dia.govt.nz,hamish.fraser@dia.govt.nz',
    description=u'OpenFisca tax and benefit system for Aotearoa',
    keywords='benefit microsimulation social tax',
    license='http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    url='https://github.com/ServiceInnovationLab/openfisca-aotearoa',
    include_package_data=True,  # Will read MANIFEST.in
    install_requires=[
        'numpy >= 1.21, < 1.22',
        'openfisca-core[web-api] >= 35, < 36',
        ],
    extras_require={
        'dev': [
            'flake8 >= 3.4, < 3.7',
            'flake8-print',
            'nose',
            'yamllint'
            ]
        },
    packages=find_packages(),
    test_suite='nose.collector',
    )
