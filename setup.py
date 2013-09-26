"""
Flask-Permissions
-------------

Simple user permissions for Flask
"""
from setuptools import setup


setup(
    name='Flask-Permissions',
    version='0.1.17',
    url='http://example.com/flask-sqlite3/',
    license='BSD',
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
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
