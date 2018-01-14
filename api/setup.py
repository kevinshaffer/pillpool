import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

setup(
    name='pillpool',
    version='0.0',
    description='pillpool api',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Kevin Shaffer',
    author_email='help@kevinshaffer.tech',
    url='',
    keywords='web pyramid pylons',
    entry_points={
        'paste.app_factory': [
            'main = pillpool:main',
        ],
    },
)
