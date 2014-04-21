"""
A simple permissions system for developers using Flask and SQLAlchemy.
"""
from setuptools import setup


setup(
    name='Flask-Permissions',
    version='0.2.3',
    url='https://github.com/raddevon/flask-permissions',
    license='MIT',
    author='Devon Campbell',
    author_email='devon@raddevon.com',
    description='Simple user permissions for Flask',
    long_description=__doc__,
    packages=['flask_permissions'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy'
    ],
    classifiers=[
        'Framework :: Flask',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
