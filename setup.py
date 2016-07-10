from setuptools import find_packages
from setuptools import setup

setup(
    name='yelp',

    version='1.0.1',

    description='yelp search results returned as image gallery',

    url='',

    author='Gil D. Kwak',
    author_email='gil@atitan.net',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    license='MIT',

    keywords='yelp',

    packages=find_packages(exclude=('venv*',)),

    install_requires=[
        'httplib2',
        'oauth2',
        'six',
    ],
)
